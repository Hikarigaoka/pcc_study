import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    def __init__(self, game, x, y, direction, color=(255, 255, 255), speed_y=0, size=None):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.color = color
        
        width = self.settings.bullet_width
        height = self.settings.bullet_height
        if size:
            width = size
            height = size
            
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = (x, y)
        
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        
        self.direction = direction
        self.speed_x = self.settings.bullet_speed * direction
        self.speed_y = speed_y
        
    def update(self):
        # Update decimal position
        self.x += self.speed_x
        self.y += self.speed_y
        
        # Update rect position
        self.rect.x = self.x
        self.rect.y = self.y
        
    def draw_bullet(self):
        if self.rect.width > 10: # Plasma
             pygame.draw.circle(self.screen, self.color, self.rect.center, self.rect.width // 2)
        else:
            pygame.draw.rect(self.screen, self.color, self.rect)
