# draw_objects.py
import pygame

RED = (255, 0, 0)
BLACK = (0, 10, 0)


def draw_bird(win, bird_sprite, bird_x, bird_y):
    win.blit(bird_sprite, (bird_x, bird_y))


def draw_pipe(win, x, y, height, gap, pipe_width, win_height):
    pygame.draw.rect(win, BLACK, (x, 0, pipe_width, height))
    pygame.draw.rect(
        win, BLACK, (x, height + gap, pipe_width, win_height - height - gap)
    )
