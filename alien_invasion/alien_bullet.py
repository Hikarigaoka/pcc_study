import pygame
from pygame.sprite import Sprite

class AlienBullet(Sprite):
    """외계인이 쏘는 탄환을 관리하는 클래스"""

    def __init__(self, ai_game, alien):
        """외계인 위치에서 탄환 객체를 생성합니다"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # (0, 0)에 탄환 rect를 만들고 올바른 위치로 옮깁니다
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
            self.settings.bullet_height)
        self.rect.midtop = alien.rect.midbottom
        
        # 탄환의 위치를 소수점 값으로 저장합니다
        self.y = float(self.rect.y)

    def update(self):
        """탄환을 화면 아래로 이동시킵니다"""
        # 탄환의 소수점 위치를 업데이트 합니다
        self.y += self.settings.alien_speed * 1.5 # 외계인보다 조금 빠르게
        # rect 위치를 업데이트 합니다
        self.rect.y = self.y

    def draw_bullet(self):
        """화면에 탄환을 그립니다"""
        pygame.draw.rect(self.screen, self.color, self.rect)
