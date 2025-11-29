import pygame
from pygame.sprite import Sprite
import random

class Helicopter(Sprite):
    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        
        self.image = pygame.Surface((60, 30))
        self.image.fill((50, 50, 50)) # Dark Grey
        self.rect = self.image.get_rect()
        
        self.rect.x = self.settings.screen_width
        self.rect.y = 50 # Fly high
        
        self.x = float(self.rect.x)
        self.has_dropped = False
        self.drop_x = random.randint(200, self.settings.screen_width - 200)
        self.game = game
        
    def update(self):
        self.x -= self.settings.helicopter_speed
        self.rect.x = self.x
        
        # Drop supply
        if not self.has_dropped and self.rect.centerx <= self.drop_x:
            self.drop_supply()
            self.has_dropped = True
            
    def drop_supply(self):
        drop_type = 'heal'
        if random.random() < 0.3: # 30% chance for weapon upgrade
            drop_type = 'weapon'
        drop = SupplyDrop(self.game, self.rect.centerx, self.rect.bottom, drop_type)
        self.game.supply_drops.add(drop)
        
    def draw(self):
        # Draw Helicopter Body (More detailed)
        pygame.draw.ellipse(self.screen, (50, 50, 50), self.rect)
        # Cockpit window
        pygame.draw.ellipse(self.screen, (100, 200, 255), (self.rect.left + 5, self.rect.top + 5, 20, 15))
        # Tail
        pygame.draw.rect(self.screen, (50, 50, 50), (self.rect.right - 5, self.rect.centery - 3, 25, 6))
        # Tail Rotor
        pygame.draw.line(self.screen, (200, 200, 200), (self.rect.right + 15, self.rect.centery - 10), (self.rect.right + 15, self.rect.centery + 10), 2)
        # Main Rotor
        pygame.draw.line(self.screen, (200, 200, 200), (self.rect.left - 10, self.rect.top), (self.rect.right + 10, self.rect.top), 3)
        # Landing Skids
        pygame.draw.line(self.screen, (30, 30, 30), (self.rect.left + 10, self.rect.bottom + 5), (self.rect.right - 10, self.rect.bottom + 5), 2)
        pygame.draw.line(self.screen, (30, 30, 30), (self.rect.left + 15, self.rect.bottom), (self.rect.left + 15, self.rect.bottom + 5), 2)
        pygame.draw.line(self.screen, (30, 30, 30), (self.rect.right - 15, self.rect.bottom), (self.rect.right - 15, self.rect.bottom + 5), 2)
        
class SupplyDrop(Sprite):
    def __init__(self, game, x, y, drop_type='heal'):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.drop_type = drop_type
        
        self.rect = pygame.Rect(0, 0, 30, 30)
        self.rect.centerx = x
        self.rect.y = y
        
        self.y = float(self.rect.y)
        
    def update(self):
        self.y += self.settings.supply_drop_speed
        self.rect.y = self.y
        
        # Destroy if hits ground
        if self.rect.bottom >= self.settings.screen_height - 50:
            self.kill()
            
    def draw(self):
        # Draw Parachute
        pygame.draw.arc(self.screen, (255, 255, 255), (self.rect.centerx - 20, self.rect.top - 40, 40, 40), 0, 3.14, 2)
        pygame.draw.line(self.screen, (255, 255, 255), (self.rect.left, self.rect.top), (self.rect.centerx, self.rect.top - 20), 1)
        pygame.draw.line(self.screen, (255, 255, 255), (self.rect.right, self.rect.top), (self.rect.centerx, self.rect.top - 20), 1)
        
        # Draw Box
        color = (255, 255, 255)
        if self.drop_type == 'weapon':
            color = (50, 50, 50) # Dark box for weapon
            
        pygame.draw.rect(self.screen, color, self.rect)
        
        # Icon
        if self.drop_type == 'heal':
            # Red Cross
            pygame.draw.rect(self.screen, (255, 0, 0), (self.rect.centerx - 3, self.rect.top + 5, 6, 20))
            pygame.draw.rect(self.screen, (255, 0, 0), (self.rect.left + 5, self.rect.centery - 3, 20, 6))
        elif self.drop_type == 'weapon':
            # Gold Bullet Icon
            pygame.draw.rect(self.screen, (255, 215, 0), (self.rect.centerx - 4, self.rect.top + 8, 8, 14))
