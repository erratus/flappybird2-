import pygame
import sys
import random
import pickle
import os
from draw_objects import draw_bird, draw_pipe
from game_states import start_screen, game_over_screen

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH, HEIGHT = 400, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

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
gravity = 0.25
jump_force = -7

# Pipe properties
pipe_width = 70
pipe_gap = 150
pipe_speed = 3
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

def save_game_state():
    global game_state, score
    data = {'game_state': game_state, 'high_score': score}
    with open(pickle_file, 'wb') as f:
        pickle.dump(data, f)

def load_game_state():
    global game_state, score
    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as f:
            data = pickle.load(f)
            game_state = data.get('game_state', START_SCREEN)
            score = data.get('high_score', 0)
    else:
        game_state = START_SCREEN
        score = 0

def main():
    global bird_y, bird_speed, score, game_state
    load_game_state()  # Load previous game state
    clock = pygame.time.Clock()
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_state == START_SCREEN:
                    game_state = PLAYING
                if event.key == pygame.K_SPACE and game_state == GAME_OVER:
                    game_state = PLAYING
                    reset_game()
                if event.key == pygame.K_ESCAPE and game_state == GAME_OVER:
                    run = False
                if event.key == pygame.K_SPACE and game_state == PLAYING:
                    bird_speed = jump_force
                if event.key == pygame.K_RETURN:
                    if game_state == START_SCREEN or game_state == GAME_OVER:
                        game_state = PLAYING
                        reset_game()

        if game_state == START_SCREEN:
            start_screen(win, WIDTH, HEIGHT, font)
        elif game_state == PLAYING:
            # Move bird
            bird_speed += gravity
            bird_y += bird_speed

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
            win.fill(WHITE)
            draw_bird(win, bird_x, bird_y, bird_width, bird_height)
            for pipe in pipes:
                draw_pipe(win, pipe[0], pipe[1], pipe[1], pipe_gap, pipe_width, HEIGHT)
            score_text = font.render(str(score), True, WHITE)
            win.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 50))
            pygame.display.update()
        elif game_state == GAME_OVER:
            game_over_screen(win, WIDTH, HEIGHT, font, score)

        # Save game state after each game action
        save_game_state()

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
