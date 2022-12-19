import sys
import pygame

from settings import Settings
from ship     import Ship

class AlienInvasion:
    """게임 전체의 자원과 동작을 관리하는 클래스"""

    def __init__(self):
        """게임을 초기화하고 게임 자원을 생성합니다"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)

    def run_game(self):
        """게임의 메인 루프를 시작합니다"""

        while True:
            self._check_events()
            self._update_screen()

    def _check_events(self):
        """키 입력과 마우스 이벤트에 반응합니다"""
        # 키보드와 마우스 이벤트를 주시합니다
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def _update_screen(self):
        """화면에 이미지를 업데이트하고 새 화면으로 그립니다"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        # 가장 최근에 그려진 화면을 표시합니다
        pygame.display.flip()

if __name__ == '__main__':
    # 게임 인스턴스를 만들고 게임을 실행합니다
    ai = AlienInvasion()
    ai.run_game()