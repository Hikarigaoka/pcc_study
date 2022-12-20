import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """우주선에서 발사하는 탄환을 관리하는 클래스"""

    def __init__(self, ai_game):
        """우주선의 현재 위치에 bullet 객체를 만듭니다"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # (0, 0)에 탄환 사각형을 만들고 정확한 위치를 지정합니다
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # 탄환 위치를 소수점 있는 값으로 저장합니다
        self.y = float(self.rect.y)
        
    def update(self):
        """탄환을 화면 위쪽으로 움직입니다"""
        # 탄환 위치를 업데이트합니다
        self.y -= self.settings.bullet_speed
        # 사각형 위치를 업데이트 합니다
        self.rect.y = self.y

    def draw_bullet(self):
        """탄환을 화면에 그립니다"""
        pygame.draw.rect(self.screen, self.color, self.rect)