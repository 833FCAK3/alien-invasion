import pygame


class Marine():

    def __init__(self, screen):
        """Initilize the marine and set his starting position."""
        self.screen = screen

        # Load marine and get his rect.
        self.image = pygame.image.load(
            "E:/Google Drive/Coding/alien_invasion/images/marine.bmp")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new marine at the center of the screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery

    def blitme(self):
        """Draw the marine at his current location."""
        self.screen.blit(self.image, self.rect)
