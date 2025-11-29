import pygame
from pygame.sprite import Sprite

class RollingObstacle(Sprite):
    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        
        self.radius = self.settings.rolling_obstacle_radius
        self.diameter = self.radius * 2
        
        self.rect = pygame.Rect(0, 0, self.diameter, self.diameter)
        self.rect.x = self.settings.screen_width
        self.rect.bottom = self.settings.screen_height - 50 # On ground
        
        self.x = float(self.rect.x)
        
    def update(self):
        self.x -= self.settings.rolling_obstacle_speed
        self.rect.x = self.x
        
    def draw(self):
        pygame.draw.circle(self.screen, self.settings.rolling_obstacle_color, self.rect.center, self.radius)
        # Draw spikes or details
        pygame.draw.circle(self.screen, (0, 0, 0), self.rect.center, 5)
