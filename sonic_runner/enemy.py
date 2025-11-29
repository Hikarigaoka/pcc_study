import pygame
from pygame.sprite import Sprite
import random
import math
from bullet import Bullet

class Enemy(Sprite):
    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.rect = pygame.Rect(0, 0, self.settings.enemy_width, self.settings.enemy_height)
        
        # Spawn at right edge
        self.rect.x = self.settings.screen_width
        self.rect.bottom = self.settings.screen_height - 50 # On ground
        
        self.x = float(self.rect.x)
        self.hp = self.settings.enemy_hp
        self.game = game
        
        # Attack state
        self.cooldown_timer = 0
        self.facing_right = False
        
        # Random Visuals
        self.color = random.choice([(0, 255, 0), (128, 0, 128), (255, 0, 0)]) # Green, Purple, Red
        self.num_eyes = random.randint(1, 3)
        self.tentacle_length = random.randint(10, 20)
        self.wiggle_offset = random.random() * 10
        
        # Buff HP based on eyes
        self.hp = self.settings.enemy_hp * self.num_eyes
        
    def update(self):
        player = self.game.player
        distance = self.rect.centerx - player.rect.centerx
        
        # AI Movement
        if abs(distance) > self.settings.enemy_attack_range:
            if distance > 0: # Player is to the left
                self.x -= self.settings.enemy_speed
                self.facing_right = False
            else: # Player is to the right
                self.x += self.settings.enemy_speed
                self.facing_right = True
        else:
            # Attack if close enough
            self.shoot()
            
        self.rect.x = self.x
        
        # Attack Logic
        if self.cooldown_timer > 0:
            self.cooldown_timer -= 1
            
    def shoot(self):
        if self.cooldown_timer <= 0:
            self.cooldown_timer = self.settings.enemy_attack_cooldown
            
            # Spawn bullet
            if self.facing_right:
                bullet_x = self.rect.right
                direction = 1
            else:
                bullet_x = self.rect.left
                direction = -1
                
            new_bullet = Bullet(self.game, bullet_x, self.rect.centery, direction, self.settings.enemy_bullet_color)
            self.game.enemy_bullets.add(new_bullet)
            
    def take_damage(self, amount):
        self.hp -= amount
        return self.hp <= 0
        
    def draw(self):
        # Alien Design (Randomized)
        
        # Body (Dome)
        pygame.draw.arc(self.screen, self.color, self.rect, 0, math.pi, 0) # Filled arc not supported directly, use ellipse/rect
        pygame.draw.ellipse(self.screen, self.color, self.rect)
        
        # Eyes
        eye_color = (0, 0, 0)
        eye_y = self.rect.top + 15
        if self.num_eyes == 1:
            pygame.draw.circle(self.screen, (255, 255, 255), (self.rect.centerx, eye_y), 8)
            pygame.draw.circle(self.screen, eye_color, (self.rect.centerx, eye_y), 3)
        elif self.num_eyes == 2:
            pygame.draw.circle(self.screen, (255, 255, 255), (self.rect.centerx - 10, eye_y), 6)
            pygame.draw.circle(self.screen, eye_color, (self.rect.centerx - 10, eye_y), 2)
            pygame.draw.circle(self.screen, (255, 255, 255), (self.rect.centerx + 10, eye_y), 6)
            pygame.draw.circle(self.screen, eye_color, (self.rect.centerx + 10, eye_y), 2)
        elif self.num_eyes == 3:
            pygame.draw.circle(self.screen, (255, 255, 255), (self.rect.centerx, eye_y - 5), 5)
            pygame.draw.circle(self.screen, eye_color, (self.rect.centerx, eye_y - 5), 2)
            pygame.draw.circle(self.screen, (255, 255, 255), (self.rect.centerx - 12, eye_y + 5), 5)
            pygame.draw.circle(self.screen, eye_color, (self.rect.centerx - 12, eye_y + 5), 2)
            pygame.draw.circle(self.screen, (255, 255, 255), (self.rect.centerx + 12, eye_y + 5), 5)
            pygame.draw.circle(self.screen, eye_color, (self.rect.centerx + 12, eye_y + 5), 2)
            
        # Tentacles (Legs) - Wiggling
        time = pygame.time.get_ticks() / 200
        for i in range(4):
            offset = (i * 10) + 5
            wiggle = math.sin(time + self.wiggle_offset + i) * 5
            start_pos = (self.rect.left + offset, self.rect.bottom - 10)
            end_pos = (self.rect.left + offset + wiggle, self.rect.bottom + self.tentacle_length)
            pygame.draw.line(self.screen, self.color, start_pos, end_pos, 3)
        
        # Draw Gun (Visual indicator of direction)
        gun_color = (50, 50, 50)
        gun_width = 15
        gun_height = 8
        if self.facing_right:
            pygame.draw.rect(self.screen, gun_color, 
                             (self.rect.right, self.rect.centery - 4, gun_width, gun_height))
        else:
            pygame.draw.rect(self.screen, gun_color, 
                             (self.rect.left - gun_width, self.rect.centery - 4, gun_width, gun_height))
            
        # Draw HP Bar
        pygame.draw.rect(self.screen, (255, 0, 0), (self.rect.x, self.rect.top - 40, self.rect.width, 5))
        hp_width = int((self.hp / self.settings.enemy_hp) * self.rect.width)
        if self.hp > 0:
            pygame.draw.rect(self.screen, (0, 255, 0), (self.rect.x, self.rect.top - 40, hp_width, 5))
