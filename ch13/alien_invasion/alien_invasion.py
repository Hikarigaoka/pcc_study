import sys

import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """게임 전체의 자원과 동작을 관리하는 클래스"""

    def __init__(self):
        """게임을 초기화하고 게임 자원을 생성합니다"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_width = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()

        self.aliens = pygame.sprite.Group()

        self._create_fleet()

    def run_game(self):
        """게임의 메인 루프를 시작합니다"""

        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_screen()
             
    def _check_events(self):
        """키 입력과 마우스 이벤트에 반응합니다"""
        # 키보드와 마우스 이벤트를 주시합니다
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
                    
    def _check_keydown_events(self, event):
        """키 입력에 반응합니다"""        
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """키에서 손을 뗄 때 반응합니다"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
    
    def _create_fleet(self):
        """외계인 함대를 만듭니다"""
        # 외계인 하나를 만들고 한 줄에 몇이 들어갈지 정합니다
        # 외계인 사이의 공간은 외계인 하나의 너비와 같습니다
        alien = Alien(self)
        alien_width = alien.rect.width
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # 외계인 첫 줄을 만듭니다
        for alien_number in range(number_aliens_x):
            # 외계인을 만들고 줄에 배치합니다
            alien = Alien(self)
            alien.x = alien_width + (2 * alien_width * alien_number)
            alien.rect.x = alien.x
            self.aliens.add(alien)

    def _fire_bullet(self):
        """새 탄환을 생성하고 bullets 그룹에 추가합니다"""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """탄환 위치를 업데이트하고 사라진 탄환을 제거합니다"""
        # 탄환 위치를 업데이트 합니다
        self.bullets.update()
        
        #사라진 탄환을 제거합니다
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _update_screen(self):
        """화면에 이미지를 업데이트하고 새 화면으로 그립니다"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)

        # 가장 최근에 그려진 화면을 표시합니다
        pygame.display.flip()

if __name__ == '__main__':
    # 게임 인스턴스를 만들고 게임을 실행합니다
    ai = AlienInvasion()
    ai.run_game()