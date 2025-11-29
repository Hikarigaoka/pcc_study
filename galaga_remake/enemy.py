import pygame
from pygame.sprite import Sprite
import math
import random
from bullet import Bullet

class Enemy(Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.rect = pygame.Rect(0, 0, self.settings.enemy_width, self.settings.enemy_height)
        self.rect.x = x
        self.rect.y = y
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.initial_x = x
        self.initial_y = y
        self.game = game
        self.diving = False
        self.dive_speed_x = 0
        self.dive_speed_y = 0
        self.tick_count = 0
        
    def update(self):
        self.tick_count += 1
        
        if self.diving:
            self.x += self.dive_speed_x
            self.y += self.dive_speed_y
            self.rect.x = self.x
            self.rect.y = self.y
            if self.rect.top > self.settings.screen_height:
                self.kill()
        else:
            # Formation movement (S-shape)
            self.x = self.initial_x + 30 * math.sin(self.tick_count * 0.05)
            self.rect.x = self.x
            
            # Random diving
            if random.random() < 0.001:
                self.start_diving()
                
            # Random shooting
            if random.random() < 0.002:
                self.shoot()
                
    def start_diving(self):
        self.diving = True
        self.dive_speed_y = 3
        # Aim towards player roughly
        if self.rect.centerx < self.game.player.rect.centerx:
            self.dive_speed_x = 1
        else:
            self.dive_speed_x = -1
            
    def shoot(self):
        bullet = Bullet(self.game, self.rect.midbottom, 1)
        self.game.enemy_bullets.add(bullet)
            
    def draw(self):
        # TIE Fighter Design
        grey = (150, 150, 150)
        dark_grey = (50, 50, 50)
        black = (0, 0, 0)
        
        # Struts (Horizontal bar)
        pygame.draw.line(self.screen, grey, 
                         (self.rect.left + 4, self.rect.centery), 
                         (self.rect.right - 4, self.rect.centery), 4)
                         
        # Central Cockpit (Ball)
        pygame.draw.circle(self.screen, grey, self.rect.center, 8)
        pygame.draw.circle(self.screen, black, self.rect.center, 4) # Window
        
        # Solar Panels (Left and Right Hexagons/Rects)
        panel_width = 6
        # Left Panel
        pygame.draw.rect(self.screen, dark_grey, 
                         (self.rect.left, self.rect.top, panel_width, self.rect.height))
        pygame.draw.rect(self.screen, grey, 
                         (self.rect.left + 2, self.rect.top + 2, panel_width - 4, self.rect.height - 4))
                         
        # Right Panel
        pygame.draw.rect(self.screen, dark_grey, 
                         (self.rect.right - panel_width, self.rect.top, panel_width, self.rect.height))
        pygame.draw.rect(self.screen, grey, 
                         (self.rect.right - panel_width + 2, self.rect.top + 2, panel_width - 4, self.rect.height - 4))

class EnemyManager:
    def __init__(self, game):
        self.game = game
        self.enemies = pygame.sprite.Group()
        self._create_fleet()
        
    def _create_fleet(self):
        # Create grid
        for row in range(4):
            for col in range(8):
                x = 100 + col * 70
                y = 50 + row * 50
                enemy = Enemy(self.game, x, y)
                self.enemies.add(enemy)
                
    def update(self):
        self.enemies.update()
        if not self.enemies:
            self._create_fleet()
        
    def draw(self):
        for enemy in self.enemies.sprites():
            enemy.draw()
