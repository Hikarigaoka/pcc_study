import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """함대에 속한 외계인 하나를 담당하는 클래스"""

    def __init__(self, ai_game):
        """외계인을 초기화하고 시작 위치를 정합니다"""
        super().__init__()
        self.screen = ai_game.screen

        #외계인 이미지를 불러오고 rect 속성을 설정합니다
        self.image = pygame.image.load('ch13/alien_invasion/images/alien.bmp')
        self.rect = self.image.get_rect()

        #외계인을 화면 좌측 상단에 배치합니다
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #외계인의 정확한 가로 위치를 저장합니다
        self.x = float(self.rect.x)