import pygame
import sys
import random
import pickle
import os
from draw_objects import draw_pipe
from game_states import start_screen, game_over_screen

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH, HEIGHT = 400, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
#font_path = "path_to_your_font.ttf" 
#font = pygame.font.Font(font_path, 36)

# Set the caption font
pygame.display.set_caption("Flappy Bird")
#pygame.display.set_caption("Flappy Bird", font=font)
BUTTON_WIDTH = 120
BUTTON_HEIGHT = 40

# assets
background_image = pygame.image.load("assets/b2g.png") 
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Bird properties
bird_width = 40
bird_height = 30
bird_x = 50
bird_y = HEIGHT // 2 - bird_height // 2
bird_speed = 5
gravity = 0.5
jump_force = -9
bird_sprite = pygame.image.load("assets/fly1.png")
bird_sprite = pygame.transform.scale(bird_sprite, (bird_width, bird_height))

# Pipe properties
pipe_width = 70
pipe_gap = 150
pipe_speed = 5
pipes = []

# Score
score = 0
font = pygame.font.SysFont(None, 50)

# Game states
START_SCREEN = 0
PLAYING = 1
GAME_OVER = 2
game_state = START_SCREEN

# File to store game state and high score
pickle_file = "game_state.pkl"


def collision(pipe):
    if bird_x + bird_width > pipe[0] and bird_x < pipe[0] + pipe_width:
        if bird_y < pipe[1] or bird_y + bird_height > pipe[1] + pipe_gap:
            return True

    return False


        
def save_game_state(highscore):
    global game_state, score
    if score>highscore:    
        data = {'game_state': game_state, 'high_score': score}
    else:
        data = {'game_state': game_state, 'high_score': highscore}
    with open(pickle_file, 'wb') as f:
        pickle.dump(data, f)


        
def load_game_state():
    global game_state, score
    try:
        if os.path.exists(pickle_file):
            with open(pickle_file, 'rb') as f:
                data = pickle.load(f)
                game_state = data.get('game_state', START_SCREEN)
                score = data.get('high_score', 0)
        else:
            game_state = START_SCREEN
            score = 0
    except Exception as e:
        print("Error occurred while loading game state:", e)
        game_state = START_SCREEN
        score = 0
    return {'game_state': game_state, 'high_score': score}

def NN():
    pass

def main():
    global bird_y, bird_speed, score, game_state
    game_data = load_game_state()
    game_state = START_SCREEN
    high = game_data['high_score']
    score = 0
    clock = pygame.time.Clock()
    run = True

    start_button_rect = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2 - 100, HEIGHT // 2 + 210, BUTTON_WIDTH, BUTTON_HEIGHT)
    NN_button_rect = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2 - 100, HEIGHT // 2 + BUTTON_HEIGHT * 3 + 140, BUTTON_WIDTH, BUTTON_HEIGHT)
    exit_button_rect = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2 + 100, HEIGHT // 2 + BUTTON_HEIGHT * 2 + 130, BUTTON_WIDTH, BUTTON_HEIGHT)


    mouse_x, mouse_y = 0, 0

    frame_counter=0
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_state == START_SCREEN:
                    game_state = PLAYING
                if event.key == pygame.K_ESCAPE and game_state == GAME_OVER:
                    run = False
                if event.key == pygame.K_SPACE and game_state == PLAYING:
                    bird_speed = jump_force
                if event.key == pygame.K_RETURN:
                    if game_state == START_SCREEN or game_state == GAME_OVER:
                        game_state = PLAYING
                        reset_game()

        if game_state == START_SCREEN:
            if high ==0:
                h1 = None
                start_screen(win, WIDTH, HEIGHT, font, frame_counter,h1)
            else:
                start_screen(win, WIDTH, HEIGHT, font, frame_counter,high)
            # Handle mouse clicks on buttons
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if start_button_rect.collidepoint(mouse_x, mouse_y):
                if pygame.mouse.get_pressed()[0]:  # Check left mouse button
                    game_state = PLAYING
                    reset_game()
            elif exit_button_rect.collidepoint(mouse_x, mouse_y):
                if pygame.mouse.get_pressed()[0]:  # Check left mouse button
                    run = False
                    reset_game()
            frame_counter += 1  # Increment the frame counter for animation
            pygame.time.Clock().tick(30)


        elif game_state == PLAYING:
            win.blit(background_image, (0, 0))
            # Move bird
            bird_speed += gravity
            bird_y += bird_speed
            if bird_y > HEIGHT:
                game_state = GAME_OVER

            # Generate pipes
            if len(pipes) == 0 or pipes[-1][0] < WIDTH - pipe_gap * 2:
                pipe_height = random.randint(100, HEIGHT - pipe_gap - 100)
                pipes.append((WIDTH, pipe_height))

            # Move pipes
            for i, pipe in enumerate(pipes):
                pipes[i] = (pipe[0] - pipe_speed, pipe[1])

                if pipe[0] + pipe_width < 0:
                    pipes.pop(i)
                    score += 1

                if collision(pipe):
                    game_state = GAME_OVER

            # Draw everything
            win.blit(bird_sprite, (bird_x, bird_y))
            for pipe in pipes:
                draw_pipe(win, pipe[0], pipe[1], pipe[1], pipe_gap, pipe_width, HEIGHT)
            score_text = font.render(str(score), True, WHITE)
            win.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 50))

            if NN_button_rect.collidepoint(mouse_x, mouse_y):
                if pygame.mouse.get_pressed()[0]:  # Check left mouse button
                    NN()

            pygame.display.update()

        elif game_state == GAME_OVER:
            win.blit(background_image, (0, 0))
            if score>high:
                game_over_screen(win, WIDTH, HEIGHT, font, score)
            else:
                game_over_screen(win, WIDTH, HEIGHT, font, high)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                bird_speed = jump_force
            save_game_state(high)
        # Save game state after each game action
        
        save_game_state(high)

        clock.tick(30)

    pygame.quit()
    sys.exit()

def reset_game():
    global bird_y, bird_speed, pipes, score
    bird_y = HEIGHT // 2 - bird_height // 2
    bird_speed = 5
    pipes = []
    score = 0

if __name__ == "__main__":
    main()