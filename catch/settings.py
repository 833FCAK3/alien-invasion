class Settings():
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Character settings.
        self.character_speed_factor = 1.5

        # Ball settings.
        self.ball_speed_factor = 3
        self.ball_radius = 50
        self.ball_color = 255, 0, 60
        self.balls_allowed = 1
