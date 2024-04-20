# game_states.py
import pygame

start_button_images = [
    pygame.image.load("assets/play1.png"),
    pygame.image.load("assets/play.png"),
]
exit_button_images = [
    pygame.image.load("assets/exit.png"),
    pygame.image.load("assets/exit1.png"),
]
ready_button_images = [
    pygame.image.load("assets/start1.png"),
    pygame.image.load("assets/start.png"),
]
home_background_image=[
    pygame.image.load("assets/homebg.png"),
    pygame.image.load("assets/homebg1.png")
]

BUTTON_WIDTH = 150
BUTTON_HEIGHT = 50
ANIMATION_SPEED = 15  # Adjust as needed for the desired animation speed


def wait_screen(win, width, height, font, framecounter):
    win.fill((202, 228, 241))
    dots = "*" * (framecounter % 4)
    waiting_text = font.render("Waiting" + dots, True, (0, 0, 0))
    win.blit(waiting_text, (width // 2 - waiting_text.get_width() // 2, height // 3))
    pygame.display.update()


def start_screen(win, width, height, font, frame_counter, score, ready):

    # Cycle through home background images
    home_background_image_index = frame_counter // ANIMATION_SPEED % len(home_background_image)
    home_bg_image = home_background_image[home_background_image_index]
    win.blit(home_bg_image, (0, 0))
    
    title_text = font.render("Flappy Bird", True, (0, 0, 0))
    win.blit(title_text, (width // 2 - title_text.get_width() // 2, height // 3-150))
    
    if score:
        score_text = font.render("High - Score: " + str(score), True, (0, 0, 0))
        win.blit(score_text, (width // 2 - score_text.get_width() // 2, height // 2 + 150))
    
    # Cycle through start button images
    start_button_image = start_button_images[
        frame_counter // ANIMATION_SPEED % len(start_button_images)
    ]
    start_button_rect = start_button_image.get_rect(center=(width // 2, height // 2))
    win.blit(start_button_image, start_button_rect.topleft)

    # Cycle through ready button images
    if ready == 0:
        ready_button_image = ready_button_images[
            frame_counter // ANIMATION_SPEED % len(ready_button_images)
        ]
        ready_button_rect = ready_button_image.get_rect(
            center=(width // 2, height // 2 + BUTTON_HEIGHT * 3+100)
        )
        win.blit(ready_button_image, ready_button_rect.topleft)

    # Cycle through exit button images
    exit_button_image = exit_button_images[
        frame_counter // ANIMATION_SPEED % len(exit_button_images)
    ]
    exit_button_rect = exit_button_image.get_rect(
        center=(width // 2, height // 2 + BUTTON_HEIGHT * 2)
    )
    win.blit(exit_button_image, exit_button_rect.topleft)

    pygame.display.update()



def game_over_screen(win, width, height, font, score):
    win.fill((202, 228, 241))
    game_over_text = font.render("Game Over", True, (0, 0, 0))
    replay_text = font.render("Press ENTER to replay", True, (0, 0, 0))
    exit_text = font.render("Press ESC to exit", True, (0, 0, 0))
    win.blit(
        game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 3)
    )
    score_text = font.render("High - Score: " + str(score), True, (0, 0, 0))
    win.blit(score_text, (width // 2 - score_text.get_width() // 2, height // 2))
    win.blit(replay_text, (width // 2 - replay_text.get_width() // 2, height // 2 + 50))
    win.blit(exit_text, (width // 2 - exit_text.get_width() // 2, height // 2 + 100))
    pygame.display.update()
