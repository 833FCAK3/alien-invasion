import pygame
from pygame.sprite import Sprite


class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        """Initialize the ship and set its starting position."""
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        #  Load the ship image and get its rect.
        self.image = pygame.image.load(
            "C:/Google Drive/Coding/alien_invasion/images/ship.bmp")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        #  Start each new ship at the center of the screen.
        self.rect.centerx = self.screen_rect.centerx
        # self.rect.centerx = self.screen_rect.centerx
        # self.rect.centery = self.screen_rect.centery
        self.rect.centery = self.screen_rect.bottom

        # Store a decimal value for the ship's center.
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)

        #  Movement flag.
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

        # Shield flag.
        self.shield_available = 1
        self.shielded = 0

    def update(self):
        """Update the ship's position based on the movement flag."""
        # Update the ship's center value, not the rect.
        if self.moving_right and self.centerx < self.screen_rect.right:
            self.centerx += self.ai_settings.ship_speed_factor
        if self.moving_left and self.centerx > 0:
            self.centerx -= self.ai_settings.ship_speed_factor
        if self.moving_up and self.centery > 0:
            self.centery -= self.ai_settings.ship_speed_factor
        if self.moving_down and self.centery < self.screen_rect.bottom:
            self.centery += self.ai_settings.ship_speed_factor

        # Update rect object from self.center.
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship on the screen."""
        self.centerx = self.screen_rect.centerx
        self.centery = self.screen_rect.bottom
