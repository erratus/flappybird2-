# game_states.py
import pygame

start_button_images = [pygame.image.load("assets/b1.png"), pygame.image.load("assets/b1C.png")]
exit_button_images = [pygame.image.load("assets/b2.png"), pygame.image.load("assets/b2C.png")]

BUTTON_WIDTH = 150
BUTTON_HEIGHT = 50
ANIMATION_SPEED = 15  # Adjust as needed for the desired animation speed

def start_screen(win, width, height, font, frame_counter):
    win.fill((202, 228, 241))
    title_text = font.render("Flappy Bird", True, (0, 0, 0))
    win.blit(title_text, (width // 2 - title_text.get_width() // 2, height // 3))

    # Cycle through start button images
    start_button_image = start_button_images[frame_counter // ANIMATION_SPEED % len(start_button_images)]
    start_button_rect = start_button_image.get_rect(center=(width // 2, height // 2))
    win.blit(start_button_image, start_button_rect.topleft)

    # Cycle through exit button images
    exit_button_image = exit_button_images[frame_counter // ANIMATION_SPEED % len(exit_button_images)]
    exit_button_rect = exit_button_image.get_rect(center=(width // 2, height // 2 + BUTTON_HEIGHT * 2))
    win.blit(exit_button_image, exit_button_rect.topleft)

    pygame.display.update()


def game_over_screen(win, width, height, font, score):
    win.fill((202, 228, 241))
    game_over_text = font.render("Game Over", True, (0, 0, 0))
    score_text = font.render("Score: " + str(score), True, (0, 0, 0))
    replay_text = font.render("Press ENTER to replay", True, (0, 0, 0))
    exit_text = font.render("Press ESC to exit", True, (0, 0, 0))
    win.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 3))
    win.blit(score_text, (width // 2 - score_text.get_width() // 2, height // 2))
    win.blit(replay_text, (width // 2 - replay_text.get_width() // 2, height // 2 + 50))
    win.blit(exit_text, (width // 2 - exit_text.get_width() // 2, height // 2 + 100))
    pygame.display.update()
