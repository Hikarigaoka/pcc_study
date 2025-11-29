import sys
import pygame
import random
from settings import Settings
from player import Player
from enemy import Enemy
from bullet import Bullet
from rolling_obstacle import RollingObstacle
from supply import Helicopter

class SonicRunner:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Sonic Runner")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 48)
        
        self.player = Player(self)
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.rolling_obstacles = pygame.sprite.Group()
        self.helicopters = pygame.sprite.Group()
        self.supply_drops = pygame.sprite.Group()
        
        self.supply_drops = pygame.sprite.Group()
        
        self.game_active = True
        self.game_over_start_time = 0
        self.score = 0
        self.start_time = 0
        
    def run_game(self):
        while True:
            self._check_events()
            
            if self.game_active:
                self.player.update()
                self._update_bullets()
                self._update_enemies()
                self._update_rolling_obstacles()
                self._update_supplies()
                self._check_collisions()
                self.score += 1
                
            self._update_screen()
            self.clock.tick(self.settings.fps)
            
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if self.game_active:
                        self.player.jump()
                elif event.key == pygame.K_SPACE:
                    if self.game_active:
                        self.player.shoot()
                    else:
                        self._reset_game()
                elif event.key == pygame.K_LEFT:
                    self.player.moving_left = True
                elif event.key == pygame.K_RIGHT:
                    self.player.moving_right = True
                elif event.key == pygame.K_DOWN:
                    if not self.player.shield_broken:
                        self.player.is_shielding = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.player.moving_left = False
                elif event.key == pygame.K_RIGHT:
                    self.player.moving_right = False
                elif event.key == pygame.K_DOWN:
                    self.player.is_shielding = False
                        
    def _update_bullets(self):
        self.bullets.update()
        self.enemy_bullets.update()
        
        # Remove off-screen bullets
        for bullet in self.bullets.copy():
            if bullet.rect.left > self.settings.screen_width or bullet.rect.right < 0:
                self.bullets.remove(bullet)
        for bullet in self.enemy_bullets.copy():
            if bullet.rect.left > self.settings.screen_width or bullet.rect.right < 0:
                self.enemy_bullets.remove(bullet)

    def _update_enemies(self):
        self.enemies.update()
                
        # Spawn new enemies
        if len(self.enemies) < 2:
            if random.random() < 0.01:
                self.enemies.add(Enemy(self))
                
    def _update_rolling_obstacles(self):
        self.rolling_obstacles.update()
        
        # Remove off-screen obstacles
        for obstacle in self.rolling_obstacles.copy():
            if obstacle.rect.right < 0:
                self.rolling_obstacles.remove(obstacle)
                
        # Spawn new obstacles
        if random.random() < 0.005: # Rare spawn
            self.rolling_obstacles.add(RollingObstacle(self))
            
    def _update_supplies(self):
        self.helicopters.update()
        self.supply_drops.update()
        
        # Remove off-screen helicopters
        for heli in self.helicopters.copy():
            if heli.rect.right < 0:
                self.helicopters.remove(heli)
                
        # Spawn Helicopter
        if random.random() < 0.002: # Very rare
            if len(self.helicopters) == 0:
                self.helicopters.add(Helicopter(self))
                
    def _check_collisions(self):
        # Player Bullets vs Enemy Body
        hits = pygame.sprite.groupcollide(self.enemies, self.bullets, False, True)
        for enemy, bullets in hits.items():
            for bullet in bullets:
                damage = 10
                if bullet.rect.width > 10: # Plasma
                    damage = self.settings.weapon_plasma_damage
                if enemy.take_damage(damage):
                    self.enemies.remove(enemy)
                    self.score += 100
                        
        # Enemy Bullets vs Player Body
        hits = pygame.sprite.spritecollide(self.player, self.enemy_bullets, True)
        for hit in hits:
            if self.player.take_damage(10):
                self.game_active = False
                self.game_over_start_time = pygame.time.get_ticks()
                
        # Rolling Obstacles vs Player
        hits = pygame.sprite.spritecollide(self.player, self.rolling_obstacles, True)
        for hit in hits:
            if self.player.take_damage(15): # High damage
                self.game_active = False
                self.game_over_start_time = pygame.time.get_ticks()
                
        # Player vs Supply Drop
        hits = pygame.sprite.spritecollide(self.player, self.supply_drops, True)
        for drop in hits:
            if drop.drop_type == 'heal':
                self.player.hp += self.settings.heal_amount
                if self.player.hp > self.settings.player_hp:
                    self.player.hp = self.settings.player_hp
            elif drop.drop_type == 'weapon':
                self.player.upgrade_weapon()
                        
    def _reset_game(self):
        self.game_active = True
        self.enemies.empty()
        self.bullets.empty()
        self.enemy_bullets.empty()
        self.rolling_obstacles.empty()
        self.helicopters.empty()
        self.supply_drops.empty()
        self.score = 0
        self.player.hp = self.settings.player_hp
        self.player.rect.x = 100
        self.player.rect.bottom = self.player.ground_y
        self.player.velocity_y = 0
        
    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        
        # Draw Ground
        pygame.draw.rect(self.screen, self.settings.ground_color, 
                         (0, self.settings.screen_height - 50, self.settings.screen_width, 50))
        
        self.player.draw()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for bullet in self.enemy_bullets.sprites():
            bullet.draw_bullet()
        for enemy in self.enemies.sprites():
            enemy.draw()
        for obstacle in self.rolling_obstacles.sprites():
            obstacle.draw()
        for heli in self.helicopters.sprites():
            heli.draw()
        for drop in self.supply_drops.sprites():
            drop.draw()
            
        # Draw Score
        score_surf = self.font.render(f"Score: {self.score // 10}", True, (255, 255, 255))
        self.screen.blit(score_surf, (20, 20))
        
        if not self.game_active:
            # Countdown
            current_time = pygame.time.get_ticks()
            elapsed_seconds = (current_time - self.game_over_start_time) // 1000
            remaining_seconds = 10 - elapsed_seconds
            
            if remaining_seconds <= 0:
                sys.exit()
                
            msg = f"Game Over! Retry? (R) - {remaining_seconds}"
            msg_surf = self.font.render(msg, True, (255, 0, 0))
            msg_rect = msg_surf.get_rect()
            msg_rect.center = self.screen.get_rect().center
            self.screen.blit(msg_surf, msg_rect)
            
        pygame.display.flip()

if __name__ == '__main__':
    game = SonicRunner()
    game.run_game()
