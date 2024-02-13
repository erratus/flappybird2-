# draw_objects.py
import pygame

RED = (255, 0, 0)
BLACK = (0, 0, 0)

def draw_bird(win, x, y, width, height):
    pygame.draw.rect(win, RED, (x, y, width, height))

def draw_pipe(win, x, y, height, gap, pipe_width, win_height):
    pygame.draw.rect(win, BLACK, (x, 0, pipe_width, height))
    pygame.draw.rect(win, BLACK, (x, height + gap, pipe_width, win_height - height - gap))
