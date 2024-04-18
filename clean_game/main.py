import pygame, random, sys
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
fps = 60
width = 864
height = 936

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Flappy Bird')


#game vars
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 150
pipe_frequency = 1500 #ms
last_pipe = pygame.time.get_ticks() - pipe_frequency
score=0
highscore=0
pipechk= False


#assets
bg = pygame.image.load('assets/bg.png')
ground_img = pygame.image.load('assets/ground.png')
font=pygame.font.Font('assets/gomarice_g_type.ttf',60)
restart=pygame.image.load('assets/restart.png')
white=(255,255,255)
black=(0,0,0)
neon_green=(21, 245, 186)
start_img=pygame.image.load('assets/play.png')
exit_img=pygame.image.load('assets/quit.png')
home=pygame.image.load('assets/home1.png')
death=pygame.mixer.Sound('assets/death.mp3')
# bgm=pygame.mixer.Sound('assets/Circuit Rampage.mp3')

def text(text,font,color,x,y):
	img=font.render(text,True,color)
	screen.blit(img,(x,y))

def reset_fn():
	pipe_group.empty()
	flyer.rect.x=100
	flyer.rect.y=int(height/2)
	score=0
	return score

class Fly(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		self.index = 0
		self.counter = 0
		for num in range(1, 4):
			img = pygame.image.load(f'assets/fly{num}.png')
			self.images.append(img)
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.vel = 0
		self.clicked = False

	def update(self):
		if flying == True:
			#gravity
			self.vel += 0.5
			if self.vel > 8:
				self.vel = 8
			if self.rect.bottom < 768:
				self.rect.y += int(self.vel)

		if game_over == False:
			#jump
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				self.vel = -10
			if pygame.mouse.get_pressed()[0] == 0:
				self.clicked = False

			#handle the animation
			self.counter += 1
			flap_cooldown = 5

			if self.counter > flap_cooldown:
				self.counter = 0
				self.index += 1
				if self.index >= len(self.images):
					self.index = 0
			self.image = self.images[self.index]

			#rotate the fly
			self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
		else:
			self.image = pygame.transform.rotate(self.images[self.index], -90)


class Pipe(pygame.sprite.Sprite):
	def __init__(self, x, y, position):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('assets/pipe.png')
		self.rect = self.image.get_rect()
		#position 1 is from the top, -1 is from the bottom
		if position == 1:
			self.image = pygame.transform.flip(self.image, False, True)
			self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
		if position == -1:
			self.rect.topleft = [x, y + int(pipe_gap / 2)]

	def update(self):
		self.rect.x -= scroll_speed
		if self.rect.right < 0:
			self.kill()

class button():
	action=False
	def __init__(self,x,y,img):
		self.img=img
		self.rect=self.img.get_rect()
		self.rect.topleft=(x,y)

	def draw(self):
		action = False
		pos=pygame.mouse.get_pos()
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0]==1:
				action=True

		screen.blit(self.img,(self.rect.x,self.rect.y))
		return action

# global class objects
fly_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()
flyer = Fly(100, int(height / 2))
fly_group.add(flyer)
restart_button=button(width//2-100, height//2-200,restart)

def home_screen():
    start_button = button(width // 2 - 300, height // 2 +200 , start_img)
    exit_button = button(width // 2 + 100, height // 2 + 200, exit_img)

    while True:
        screen.blit(home, (0, 0))
        start_action = start_button.draw()
        exit_action = exit_button.draw()
        text('Fly_Jack',font,black,int(width)/2-180,50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if start_action:
            return True
        elif exit_action:
            pygame.quit()
            sys.exit()

        pygame.display.update()
        clock.tick(fps)

def end_screen():
    restart_button = button(width // 2 - 100, height // 2 - 50, restart)
    exit_button = button(width // 2 - 100, height // 2 + 100, exit_img)

    while True:
        # screen.blit(bg, (0, 0))
        text('GAME OVER',font,neon_green,int(width)/2-180,100)
        restart_action = restart_button.draw()
        exit_action = exit_button.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if restart_action:
            return True
        elif exit_action:
            pygame.quit()
            sys.exit()

        pygame.display.update()
        clock.tick(fps)

def main_game():
    global ground_scroll, scroll_speed, flying, game_over, \
        pipe_gap, pipe_frequency, last_pipe, score, pipechk,highscore
    run = True
    while run:
        # bgm.play()

        clock.tick(fps)

        # draw background
        screen.blit(bg, (0, 0))

        fly_group.draw(screen)
        fly_group.update()
        pipe_group.draw(screen)

        # draw the ground
        screen.blit(ground_img, (ground_scroll, 768))

        # score
        if len(pipe_group) > 0:
            if fly_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left \
                    and fly_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right \
                    and pipechk == False:
                pipechk = True
            if pipechk == True:
                if fly_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                    score += 1
                    pipechk = False

        text(str(score), font, white, int(width) / 2, 20)

        # collision check
        if pygame.sprite.groupcollide(fly_group, pipe_group, False, False) or flyer.rect.top < 0:
            game_over = True

        # sprite flight check
        if flyer.rect.bottom >= 768:
            game_over = True
            flying = False

        if game_over == False and flying == True:

            # generate new pipes
            time_now = pygame.time.get_ticks()
            if time_now - last_pipe > pipe_frequency:
                pipe_height = random.randint(-100, 100)
                btm_pipe = Pipe(width, int(height / 2) + pipe_height, -1)
                top_pipe = Pipe(width, int(height / 2) + pipe_height, 1)
                pipe_group.add(btm_pipe)
                pipe_group.add(top_pipe)
                last_pipe = time_now

            # draw and scroll the ground
            ground_scroll -= scroll_speed
            if abs(ground_scroll) > 35:
                ground_scroll = 0

            pipe_group.update()

        if game_over == True:
            # bgm.stop()
            death.play()
            if end_screen():
                game_over = False
                if highscore<score:
                    highscore=score
                    print('highscore',highscore)
                score = reset_fn()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
                flying = True

        pygame.display.update()

    pygame.quit()

# Call main_game function
while True:
    if home_screen():
        main_game()