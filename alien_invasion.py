from pygame.sprite import Group
import game_functions as gf
import pygame
from settings import Settings
from game_stats import GameStats
from button import Button
from ship import Ship
from scoreboard import Scoreboard
from shield import Shield


def run_game():
    # Initialize pygame, settings and screen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Make the Play button.
    play_button = Button(ai_settings, screen, "Play")

    # Create an instance to store game statistics and create a scoreboard.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # Make a ship, a group of bullets and a group of aliens.
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    stars = Group()
    drops = Group()
    shield = Shield(ai_settings, screen, ship)

    # Create the fleet of aliens.
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Create a grid of starts.
    gf.create_star_grid(ai_settings, screen, stars, aliens)

    # Create rain.
    gf.create_rain(ai_settings, screen, drops)

    # Start the main loop for the game.
    while True:
        gf.check_events(ai_settings, screen, stats, sb,
                        play_button, ship, aliens, bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats,
                              sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen,
                             sb, ship, aliens, bullets)
            gf.update_drops(ai_settings, drops, screen)

        gf.update_screen(ai_settings, screen, stats, sb, stars,
                         drops, ship, aliens, bullets, play_button, shield)


run_game()
