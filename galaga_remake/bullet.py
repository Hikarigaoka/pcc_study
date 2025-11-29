import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    def __init__(self, game, pos, direction):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.center = pos
        self.y = float(self.rect.y)
        self.direction = direction # -1 for up (player), 1 for down (enemy)
        self.color = self.settings.bullet_color
        
    def update(self):
        self.y += self.settings.bullet_speed * self.direction
        self.rect.y = self.y
        
    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
