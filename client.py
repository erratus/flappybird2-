import pygame
import socket
import pickle

# Server configuration
SERVER = '127.0.0.1'
PORT = 5050

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

# Socket initialization
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Send player input to the server
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                client.send("JUMP".encode())

    # Receive updated game state from the server
    try:
        game_state_data = client.recv(4096)
        game_state = pickle.loads(game_state_data)

        # Extract relevant information from the game state dictionary
        bird_y = game_state['bird_y']
        pipes = game_state['pipes']
        score = game_state['score']

        # Update game display based on the received game state
        win.fill(WHITE)
        pygame.draw.rect(win, RED, (bird_x, bird_y, bird_width, bird_height))
        for pipe in pipes:
            pygame.draw.rect(win, BLACK, (pipe['x'], 0, pipe_width, pipe['y']))
            pygame.draw.rect(win, BLACK, (pipe['x'], pipe['y'] + pipe_gap, pipe_width, HEIGHT - pipe['y'] - pipe_gap))
        font = pygame.font.SysFont(None, 50)
        score_text = font.render(str(score), True, WHITE)
        win.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 50))

    except Exception as e:
        print("Error receiving game state:", e)
        break

    pygame.display.update()

pygame.quit()
