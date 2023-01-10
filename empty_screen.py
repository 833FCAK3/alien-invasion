import pygame
import sys


def run_game():

    # Initialize game and create a screen object.
    pygame.init()
    screen = pygame.display.set_mode((800, 640))
    pygame.display.set_caption("Alien Invasion")

    # Start the main loop for the game.
    while True:

        # Watch for keyboard and mouse events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                print(event.key)

        # Make the most recently drawn screen visible.
        pygame.display.flip()


run_game()
