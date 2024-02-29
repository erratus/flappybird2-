# game_states.py
import pygame
import random

def start_screen(win, width, height, font):
    win.fill((255, 255, 255))
    title_text = font.render("Flappy Bird", True, (0, 0, 0))
    instruction_text = font.render("Press SPACE to jump", True, (0, 0, 0))
    start_text = font.render("Press ENTER to start", True, (0, 0, 0))
    win.blit(title_text, (width // 2 - title_text.get_width() // 2, height // 3))
    win.blit(instruction_text, (width // 2 - instruction_text.get_width() // 2, height // 2))
    win.blit(start_text, (width // 2 - start_text.get_width() // 2, height // 2 + 50))
    pygame.display.update()

def game_over_screen(win, width, height, font, score):
    win.fill((255, 255, 255))
    game_over_text = font.render("Game Over", True, (0, 0, 0))
    score_text = font.render("Score: " + str(score), True, (0, 0, 0))
    replay_text = font.render("Press ENTER to replay", True, (0, 0, 0))
    exit_text = font.render("Press ESC to exit", True, (0, 0, 0))
    win.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 3))
    win.blit(score_text, (width // 2 - score_text.get_width() // 2, height // 2))
    win.blit(replay_text, (width // 2 - replay_text.get_width() // 2, height // 2 + 50))
    win.blit(exit_text, (width // 2 - exit_text.get_width() // 2, height // 2 + 100))
    pygame.display.update()
