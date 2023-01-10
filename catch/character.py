import pygame


class Character():

    def __init__(self, ai_settings, screen):
        """Initialize the character and set its starting position."""
        self.screen = screen
        self.ai_settings = ai_settings

        #  Load the character image and get its rect.
        self.image = pygame.image.load(
            "C:/Google Drive/Coding/alien_invasion/catch/images/character.bmp")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        #  Start each new character at the bottom center of the screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery

        # Store a decimal value for the character's center.
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)

        #  Movement flag.
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """Update the character's position based on the movement flag."""
        # Update the character's center value, not the rect.
        if self.moving_right and self.centerx < self.screen_rect.right:
            self.centerx += self.ai_settings.character_speed_factor
        if self.moving_left and self.centerx > 0:
            self.centerx -= self.ai_settings.character_speed_factor
        if self.moving_up and self.centery > 0:
            self.centery -= self.ai_settings.character_speed_factor
        if self.moving_down and self.centery < self.screen_rect.bottom:
            self.centery += self.ai_settings.character_speed_factor

        # Update rect object from self.center.
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery

    def blitme(self):
        """Draw the character at its current location."""
        self.screen.blit(self.image, self.rect)
