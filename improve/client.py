import socket
import pickle
import pygame
from pygame.locals import *
import sys

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH, HEIGHT = 400, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Client")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Bird properties
bird_width = 40
bird_height = 30
bird_speed = 5
gravity = 0.25
jump_force = -7

# Pipe properties
pipe_width = 70
pipe_gap = 150

# Clock
clock = pygame.time.Clock()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 5050))

def receive_game_state():
    try:
        data = client.recv(4096)
        if not data:
            return None
        game_state = pickle.loads(data)
        return game_state
    except Exception as e:
        print(e)
        return None

def main():
    global bird_y, bird_speed
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    bird_speed = jump_force

        # Send jump action to server
        client.send("JUMP".encode())

        # Receive game state from server
        game_state = receive_game_state()

        if game_state:
            bird_y = game_state['bird_y']
            pipes = game_state['pipes']

            # Draw everything
            win.fill(WHITE)
            pygame.draw.rect(win, GREEN, (50, bird_y, bird_width, bird_height))
            for pipe in pipes:
                pygame.draw.rect(win, GREEN, (pipe['x'], 0, pipe_width, pipe['y']))
                pygame.draw.rect(win, GREEN, (pipe['x'], pipe['y'] + pipe_gap, pipe_width, HEIGHT - pipe['y'] - pipe_gap))
            pygame.display.update()

        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
