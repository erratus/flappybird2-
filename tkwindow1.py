import tkinter as tk
import pygame
from pygame.locals import *
import random
import sys
import io
from PIL import Image, ImageTk

class FlappyBirdApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Flappy Bird")
        self.master.geometry("400x600")

        self.canvas = tk.Canvas(master, width=400, height=600)
        self.canvas.pack()

        self.images = []  # List to store references to images
        self.game_running = False   

        self.start_game()  # Start the game when initialized

    def start_game(self):
        self.game_running = True
        self.master.bind("<space>", self.jump)

        # Initialize Pygame
        pygame.init()
        clock = pygame.time.Clock()

        # Set up Pygame window
        win = pygame.Surface((400, 600))

        # Colors
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        RED = (255, 0, 0)

        # Bird properties
        bird_width = 40
        bird_height = 30
        bird_x = 50
        bird_y = 300
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

        def draw_bird(x, y):
            pygame.draw.rect(win, RED, (x, y, bird_width, bird_height))

        def draw_pipe(x, y, height):
            pygame.draw.rect(win, BLACK, (x, 0, pipe_width, height))
            pygame.draw.rect(win, BLACK, (x, height + pipe_gap, pipe_width, 600 - height - pipe_gap))

        def draw_score(score):
            score_text = font.render(str(score), True, WHITE)
            win.blit(score_text, (400 // 2 - score_text.get_width() // 2, 50))

        def collision(pipe):
            if bird_x + bird_width > pipe[0] and bird_x < pipe[0] + pipe_width:
                if bird_y < pipe[1] or bird_y + bird_height > pipe[1] + pipe_gap:
                    return True
            return False

        run = True
        while self.game_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bird_speed = jump_force

            # Move bird
            bird_speed += gravity
            bird_y += bird_speed

            # Generate pipes
            if len(pipes) == 0 or pipes[-1][0] < 400 - pipe_gap * 2:
                pipe_height = random.randint(100, 450)
                pipes.append((400, pipe_height))

            # Move pipes
            for i, pipe in enumerate(pipes):
                pipes[i] = (pipe[0] - pipe_speed, pipe[1])

                if pipe[0] + pipe_width < 0:
                    pipes.pop(i)
                    score += 1

                if collision(pipe):
                    self.end_game(score)
                    return

            # Draw everything
            win.fill(WHITE)
            draw_bird(bird_x, bird_y)
            for pipe in pipes:
                draw_pipe(pipe[0], pipe[1], pipe[1])
            draw_score(score)

            # Convert Pygame surface to Tkinter PhotoImage
            image = pygame.image.tostring(win, 'RGB')
            img = Image.frombytes('RGB', (400, 600), image)
            photo = ImageTk.PhotoImage(img)
            self.images.append(photo)  # Keep a reference to the image

            # Display on canvas
            self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            self.master.update()

            clock.tick(30)

        pygame.quit()
        sys.exit()

    def end_game(self, score):
        self.game_running = False
        self.canvas.delete("all")

        # Display end screen
        end_text = f"Game Over\nScore: {score}\nPress Enter to Play Again"
        self.canvas.create_text(200, 300, text=end_text, font=("Arial", 20), anchor=tk.CENTER)

    def jump(self, event):
        pass  # Placeholder for jump action, can be implemented later

def main():
    root = tk.Tk()
    app = FlappyBirdApp(root)
    root.bind("<Return>", lambda event: app.start_game())  # Bind start_game to Enter key
    root.mainloop()

if __name__ == "__main__":
    main()
