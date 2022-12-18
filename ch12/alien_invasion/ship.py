import pygame

class Ship:
    """우주선을 관리하는 클래스"""

    def __init__(self, ai_game):
        """우주선을 초기화하고 시작 위치를 결정합니다"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # 우주선 이미지를 불러오고 그 사각형을 가져옵니다
        self.image = pygame.image.load('ch12/alien_invasion/images/ship.bmp')
        self.rect = self.image.get_rect()

        # 우주선을 불러올 때마다 화면의 아래쪽 중앙에서 시작합니다
        self.rect.midbottom = self.screen_rect.midbottom
    
    def blitme(self):
        """현재 위치에 우주선을 그립니다"""
        self.screen.blit(self.image, self.rect)