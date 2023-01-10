import pygame


class Shield():

    def __init__(self, ai_settings, screen, ship):
        """Initialize shield attributes."""
    #     self.screen = screen
    #     self.screen_rect = screen.get_rect()

    #     self.circle = pygame.draw.circle(
    #         screen, (255, 0, 0), (ship.rect.centery, ship.rect.centerx), 20)

    #     self.x = float(self.circle.x)
    #     self.y = float(self.circle.y)

    # def update(self, ship):
    #     """Keep the shield centered on ship."""
    #     self.x = ship.rect.x
    #     self.y = ship.rect.y

    #     self.circle.x = self.x
    #     self.circle.y = self.y

    def draw_shield(self, ai_settings, screen, ship):
        """Draw the shield to the screen."""
        if ship.shielded == 1 and (ai_settings.end - ai_settings.start) <= 3:
            pygame.draw.circle(
                screen, (255, 0, 0), (ship.rect.centerx, ship.rect.centery), 50)
        if ship.shielded == 1 and (ai_settings.end - ai_settings.start) > 3:
            ship.shielded = 0
