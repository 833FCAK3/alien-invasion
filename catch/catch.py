from pygame.sprite import Group
import game_functions as gf
import pygame
from settings import Settings
from character import Character


def run_game():
    # Initialize pygame, settings and screen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Catch")

    # Make a character and a ball.
    character = Character(ai_settings, screen)
    # ball = Ball()

    # Start the main loop for the game.
    while True:
        # gf.check_events(ai_settings, screen, ship, bullets)
        character.update()


run_game()
