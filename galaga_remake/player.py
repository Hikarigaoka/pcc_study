import pygame
from bullet import Bullet

class Player:
    def __init__(self, game):
        self.screen = game.screen
        self.settings = game.settings
        self.rect = pygame.Rect(0, 0, self.settings.player_width, self.settings.player_height)
        self.rect.midbottom = self.screen.get_rect().midbottom
        self.rect.y -= 20
        self.x = float(self.rect.x)
        self.moving_right = False
        self.moving_left = False
        self.game = game
        self.hp = self.settings.player_max_hp
        
    def take_damage(self, amount):
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0
        return self.hp <= 0
        
    def update(self):
        if self.moving_right and self.rect.right < self.screen.get_rect().right:
            self.x += self.settings.player_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.player_speed
        self.rect.x = self.x
        
    def draw(self):
        # X-Wing Design
        color = (200, 200, 200) # Light grey
        red = (255, 50, 50)
        
        # Fuselage (Body)
        pygame.draw.rect(self.screen, color, 
                         (self.rect.centerx - 4, self.rect.top, 8, self.rect.height))
        
        # Wings (X shape)
        # Using polygons for thicker, angled wings
        # Top-left wing
        pygame.draw.polygon(self.screen, color, [
            (self.rect.centerx, self.rect.centery),
            (self.rect.left, self.rect.top + 10),
            (self.rect.left, self.rect.bottom - 10)
        ])
        # Top-right wing
        pygame.draw.polygon(self.screen, color, [
            (self.rect.centerx, self.rect.centery),
            (self.rect.right, self.rect.top + 10),
            (self.rect.right, self.rect.bottom - 10)
        ])
        
        # Engines (Red tips)
        pygame.draw.rect(self.screen, red, (self.rect.left, self.rect.top + 5, 4, 15))
        pygame.draw.rect(self.screen, red, (self.rect.right - 4, self.rect.top + 5, 4, 15))
        pygame.draw.rect(self.screen, red, (self.rect.left, self.rect.bottom - 20, 4, 15))
        pygame.draw.rect(self.screen, red, (self.rect.right - 4, self.rect.bottom - 20, 4, 15))
        
        # Cockpit
        pygame.draw.rect(self.screen, (50, 50, 50), (self.rect.centerx - 2, self.rect.centery - 5, 4, 10))
        
        # Draw HP Bar
        self.draw_hp_bar()
        
    def draw_hp_bar(self):
        bar_width = 40
        bar_height = 5
        fill_width = int((self.hp / self.settings.player_max_hp) * bar_width)
        
        # Background bar (Red)
        pygame.draw.rect(self.screen, (255, 0, 0), 
                         (self.rect.centerx - bar_width // 2, self.rect.bottom + 5, bar_width, bar_height))
        # Health bar (Green)
        if self.hp > 0:
            pygame.draw.rect(self.screen, (0, 255, 0), 
                             (self.rect.centerx - bar_width // 2, self.rect.bottom + 5, fill_width, bar_height))
        
    def check_keydown(self, event):
        if event.key == pygame.K_RIGHT:
            self.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.moving_left = True
        elif event.key == pygame.K_SPACE:
            self.shoot()
            
    def check_keyup(self, event):
        if event.key == pygame.K_RIGHT:
            self.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.moving_left = False
            
    def shoot(self):
        if len(self.game.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self.game, self.rect.midtop, -1)
            self.game.bullets.add(new_bullet)
