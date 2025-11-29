import pygame
from pygame.sprite import Sprite
import random

class Obstacle(Sprite):
    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        
        # Randomize obstacle type (height)
        height = random.randint(30, 70)
        self.rect = pygame.Rect(0, 0, self.settings.obstacle_width, height)
        
        # Spawn at right edge
        self.rect.x = self.settings.screen_width
        self.rect.bottom = self.settings.screen_height - 50 # On ground
        
        self.x = float(self.rect.x)
        
    def update(self):
        self.x -= self.settings.obstacle_speed
        self.rect.x = self.x
        
    def draw(self):
        # Draw as a triangle (spike)
        points = [
            (self.rect.left, self.rect.bottom),
            (self.rect.centerx, self.rect.top),
            (self.rect.right, self.rect.bottom)
        ]
        pygame.draw.polygon(self.screen, self.settings.obstacle_color, points)
