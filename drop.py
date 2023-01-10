import pygame
from pygame.sprite import Sprite


class Drop(Sprite):
    """A class to create an imitation of a rain."""

    def __init__(self, ai_settings, screen):
        """Initialize the drop and set its starting position."""
        super(Drop, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the image and set its rect attribute.
        self.image = pygame.image.load(
            "C:/Google Drive/Coding/alien_invasion/images/drop.bmp")
        self.rect = self.image.get_rect()

        # Start each new drop near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y - self.rect.height

        # Store the drops's exact position.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        """Move the drop diagonally."""
        self.x += self.ai_settings.drop_speed_x
        self.y += self.ai_settings.drop_speed_y
        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        """Draw the drop at its current location."""
        self.screen.blit(self.image, self.rect)
