import pygame
from pygame.sprite import Sprite
from bullet import Bullet
import random

class Player:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.rect = pygame.Rect(100, 0, self.settings.player_width, self.settings.player_height)
        self.ground_y = self.settings.screen_height - 50
        self.rect.bottom = self.ground_y
        
        self.velocity_y = 0
        self.is_jumping = False
        self.moving_left = False
        self.moving_right = False
        
        self.hp = self.settings.player_hp
        self.shield_hp = self.settings.shield_max_hp
        self.shield_broken = False
        self.shield_cooldown_timer = 0
        
        self.weapon_level = 1
        self.upgrade_timer = 0
        
        self.facing_right = True
        self.is_shielding = False
        
        # Attack state
        self.cooldown_timer = 0
        
    def update(self):
        # Shield Logic
        if self.shield_broken:
            self.is_shielding = False
            self.shield_cooldown_timer -= 1
            if self.shield_cooldown_timer <= 0:
                self.shield_broken = False
                self.shield_hp = self.settings.shield_max_hp // 2 # Recover with half HP
        elif not self.is_shielding and self.shield_hp < self.settings.shield_max_hp:
            self.shield_hp += self.settings.shield_recovery_rate
            if self.shield_hp > self.settings.shield_max_hp:
                self.shield_hp = self.settings.shield_max_hp
                
        # Passive HP Regeneration
        if self.hp < self.settings.player_hp and self.hp > 0:
            self.hp += self.settings.player_hp_recovery_rate
            if self.hp > self.settings.player_hp:
                self.hp = self.settings.player_hp
                
        # Weapon Upgrade Timer
        if self.upgrade_timer > 0:
            self.upgrade_timer -= 1
            if self.upgrade_timer <= 0:
                self.weapon_level = 1
                
        # Horizontal Movement
        if self.moving_right and self.rect.right < self.settings.screen_width:
            self.rect.x += self.settings.player_speed
            self.facing_right = True
        if self.moving_left and self.rect.left > 0:
            self.rect.x -= self.settings.player_speed
            self.facing_right = False
            
        # Apply gravity
        self.velocity_y += self.settings.gravity
        self.rect.y += self.velocity_y
        
        # Check ground collision
        if self.rect.bottom >= self.ground_y:
            self.rect.bottom = self.ground_y
            self.velocity_y = 0
            self.is_jumping = False
            
        # Attack Logic
        if self.cooldown_timer > 0:
            self.cooldown_timer -= 1
            
    def jump(self):
        if not self.is_jumping:
            self.velocity_y = self.settings.jump_strength
            self.is_jumping = True
            
    def shoot(self):
        if self.cooldown_timer <= 0:
            self.cooldown_timer = self.settings.attack_cooldown
            
            # Spawn bullet
            if self.facing_right:
                bullet_x = self.rect.right
                direction = 1
            else:
                bullet_x = self.rect.left
                direction = -1
                
            if self.weapon_level == 1:
                new_bullet = Bullet(self.game, bullet_x, self.rect.centery, direction, self.settings.player_bullet_color)
                self.game.bullets.add(new_bullet)
            elif self.weapon_level == 2:
                # Double Shot
                bullet1 = Bullet(self.game, bullet_x, self.rect.centery - 10, direction, self.settings.player_bullet_color)
                bullet2 = Bullet(self.game, bullet_x, self.rect.centery + 10, direction, self.settings.player_bullet_color)
                self.game.bullets.add(bullet1)
                self.game.bullets.add(bullet2)
            elif self.weapon_level == 3:
                # Spread Shot
                b1 = Bullet(self.game, bullet_x, self.rect.centery, direction, self.settings.player_bullet_color, speed_y=0)
                b2 = Bullet(self.game, bullet_x, self.rect.centery, direction, self.settings.player_bullet_color, speed_y=-2)
                b3 = Bullet(self.game, bullet_x, self.rect.centery, direction, self.settings.player_bullet_color, speed_y=2)
                self.game.bullets.add(b1)
                self.game.bullets.add(b2)
                self.game.bullets.add(b3)
            elif self.weapon_level == 4:
                # Plasma Cannon
                plasma = Bullet(self.game, bullet_x, self.rect.centery, direction, self.settings.weapon_plasma_color, size=20)
                plasma.speed_x = self.settings.weapon_plasma_speed * direction # Slower but bigger
                self.game.bullets.add(plasma)
            
    def upgrade_weapon(self):
        if self.weapon_level < 4:
            self.weapon_level += 1
        else:
            self.weapon_level = 4 # Max level
        self.upgrade_timer = self.settings.weapon_upgrade_duration
            
    def take_damage(self, amount):
        if self.is_shielding:
            self.shield_hp -= amount
            if self.shield_hp <= 0:
                self.shield_hp = 0
                self.shield_broken = True
                self.shield_cooldown_timer = self.settings.shield_break_cooldown
            return False
        self.hp -= amount
        return self.hp <= 0
            
    def draw(self):
        # Mandalorian Design
        beskar_silver = (192, 192, 192)
        dark_grey = (50, 50, 50)
        cape_color = (100, 80, 70) # Brownish
        visor_black = (0, 0, 0)
        
        # Cape (Behind)
        if self.facing_right:
            pygame.draw.polygon(self.screen, cape_color, [
                (self.rect.left + 5, self.rect.top + 10),
                (self.rect.left - 5, self.rect.bottom - 10),
                (self.rect.left + 10, self.rect.bottom - 10)
            ])
        else:
            pygame.draw.polygon(self.screen, cape_color, [
                (self.rect.right - 5, self.rect.top + 10),
                (self.rect.right + 5, self.rect.bottom - 10),
                (self.rect.right - 10, self.rect.bottom - 10)
            ])
        
        # Jetpack Flame (if jumping)
        if self.is_jumping:
            flame_color = (255, 100, 0) # Orange
            pygame.draw.polygon(self.screen, flame_color, [
                (self.rect.left + 10, self.rect.bottom - 10),
                (self.rect.right - 10, self.rect.bottom - 10),
                (self.rect.centerx, self.rect.bottom + random.randint(5, 15))
            ])
        
        # Legs (Armor)
        pygame.draw.rect(self.screen, beskar_silver, (self.rect.left + 5, self.rect.bottom - 25, 12, 25))
        pygame.draw.rect(self.screen, beskar_silver, (self.rect.right - 17, self.rect.bottom - 25, 12, 25))
        
        # Body (Chest Plate)
        pygame.draw.rect(self.screen, dark_grey, (self.rect.left + 5, self.rect.top + 15, self.rect.width - 10, 30)) # Undersuit
        pygame.draw.rect(self.screen, beskar_silver, (self.rect.left + 5, self.rect.top + 15, self.rect.width - 10, 20)) # Chest plate
        
        # Head (Helmet)
        head_rect = pygame.Rect(self.rect.centerx - 12, self.rect.top, 24, 24)
        pygame.draw.ellipse(self.screen, beskar_silver, head_rect)
        
        # T-Visor
        visor_width = 16
        visor_height = 4
        vertical_width = 4
        vertical_height = 12
        
        if self.facing_right:
            # Horizontal
            pygame.draw.rect(self.screen, visor_black, (head_rect.right - 18, head_rect.centery - 4, visor_width, visor_height))
            # Vertical
            pygame.draw.rect(self.screen, visor_black, (head_rect.right - 12, head_rect.centery - 4, vertical_width, vertical_height))
        else:
            # Horizontal
            pygame.draw.rect(self.screen, visor_black, (head_rect.left + 2, head_rect.centery - 4, visor_width, visor_height))
            # Vertical
            pygame.draw.rect(self.screen, visor_black, (head_rect.left + 8, head_rect.centery - 4, vertical_width, vertical_height))
            
        # Arms (Gauntlets)
        pygame.draw.rect(self.screen, beskar_silver, (self.rect.left - 2, self.rect.top + 18, 8, 18))
        pygame.draw.rect(self.screen, beskar_silver, (self.rect.right - 6, self.rect.top + 18, 8, 18))
        
        # Draw Gun (Rifle/Pistol)
        gun_color = (30, 30, 30)
        if self.weapon_level > 1:
            gun_color = (255, 215, 0) # Gold
            
        if self.facing_right:
            pygame.draw.rect(self.screen, gun_color, (self.rect.right + 4, self.rect.centery + 5, 15, 5))
            if self.weapon_level > 1: 
                pygame.draw.rect(self.screen, gun_color, (self.rect.right + 4, self.rect.centery, 15, 5))
        else:
            pygame.draw.rect(self.screen, gun_color, (self.rect.left - 19, self.rect.centery + 5, 15, 5))
            if self.weapon_level > 1: 
                pygame.draw.rect(self.screen, gun_color, (self.rect.left - 19, self.rect.centery, 15, 5))
                             
        # Draw Shield
        if self.is_shielding:
            shield_color = (0, 100, 255) # Deep Blue
            if self.facing_right:
                pygame.draw.arc(self.screen, shield_color, 
                                (self.rect.right - 15, self.rect.top - 15, 50, self.rect.height + 30), 
                                -1.5, 1.5, 5)
            else:
                pygame.draw.arc(self.screen, shield_color, 
                                (self.rect.left - 35, self.rect.top - 15, 50, self.rect.height + 30), 
                                1.6, 4.7, 5)
            
        # Draw HP Bar (Higher)
        bar_y = self.rect.top - 40
        pygame.draw.rect(self.screen, (255, 0, 0), (self.rect.x, bar_y, self.rect.width, 5))
        hp_width = int((self.hp / self.settings.player_hp) * self.rect.width)
        if self.hp > 0:
            pygame.draw.rect(self.screen, (0, 255, 0), (self.rect.x, bar_y, hp_width, 5))
            
        # Draw Shield Bar
        shield_bar_y = self.rect.top - 33
        pygame.draw.rect(self.screen, (50, 50, 50), (self.rect.x, shield_bar_y, self.rect.width, 3))
        shield_width = int((self.shield_hp / self.settings.shield_max_hp) * self.rect.width)
        if self.shield_hp > 0:
            shield_color = (0, 200, 255) if not self.shield_broken else (100, 100, 100)
            pygame.draw.rect(self.screen, shield_color, (self.rect.x, shield_bar_y, shield_width, 3))
