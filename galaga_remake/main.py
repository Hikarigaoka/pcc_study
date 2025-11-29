import sys
import pygame
from settings import Settings
from player import Player
from enemy import EnemyManager
from starfield import Starfield

class GalagaGame:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Galaga Remake")
        self.clock = pygame.time.Clock()
        
        self.bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        
        self.player = Player(self)
        self.enemy_manager = EnemyManager(self)
        self.starfield = Starfield(self)
        
        self.game_active = True
        self.font = pygame.font.SysFont(None, 48)
        
    def run_game(self):
        while True:
            self._check_events()
            
            if self.game_active:
                self.player.update()
                self.bullets.update()
                self.enemy_bullets.update()
                self.enemy_manager.update()
                self.starfield.update()
                self._check_collisions()
                
            self._update_screen()
            self.clock.tick(self.settings.fps)
            
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.player.check_keydown(event)
                if not self.game_active and event.key == pygame.K_r:
                    self._reset_game()
            elif event.type == pygame.KEYUP:
                self.player.check_keyup(event)
                
    def _reset_game(self):
        self.game_active = True
        self.player.hp = self.settings.player_max_hp
        self.bullets.empty()
        self.enemy_bullets.empty()
        self.enemy_manager.enemies.empty()
        self.enemy_manager._create_fleet()
        self.player.rect.midbottom = self.screen.get_rect().midbottom
        self.player.rect.y -= 20
        self.player.x = float(self.player.rect.x)
                
    def _check_collisions(self):
        # Remove bullets off screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        for bullet in self.enemy_bullets.copy():
            if bullet.rect.top >= self.settings.screen_height:
                self.enemy_bullets.remove(bullet)
                
        # Player bullets hit enemies
        pygame.sprite.groupcollide(self.bullets, self.enemy_manager.enemies, True, True)
        
        # Enemy bullets hit player
        # Check for collisions and remove the bullet (True)
        hits = pygame.sprite.spritecollide(self.player, self.enemy_bullets, True)
        for hit in hits:
            print("Player Hit by Bullet!")
            if self.player.take_damage(10):
                print("Game Over!")
                self.game_active = False
            
        # Enemies hit player
        # Check for collisions and remove the enemy (True)
        hits = pygame.sprite.spritecollide(self.player, self.enemy_manager.enemies, True)
        for hit in hits:
            print("Player Hit by Enemy!")
            if self.player.take_damage(20):
                print("Game Over!")
                self.game_active = False
                
    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.starfield.draw()
        self.player.draw()
        self.enemy_manager.draw()
        
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for bullet in self.enemy_bullets.sprites():
            bullet.draw_bullet()
            
        if not self.game_active:
            msg = "Game Over - Press R to Retry"
            msg_image = self.font.render(msg, True, (255, 0, 0))
            msg_rect = msg_image.get_rect()
            msg_rect.center = self.screen.get_rect().center
            self.screen.blit(msg_image, msg_rect)
            
        pygame.display.flip()

if __name__ == '__main__':
    game = GalagaGame()
    game.run_game()
