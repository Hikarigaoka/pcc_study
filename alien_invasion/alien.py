import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """함대에 속한 외계인 하나를 담당하는 클래스"""

    def __init__(self, ai_game):
        """외계인을 초기화하고 시작 위치를 정합니다"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        #외계인 이미지를 불러오고 rect 속성을 설정합니다
        self.image = pygame.image.load('/Users/rex/Documents/GitHub/pcc_study/alien_invasion/images/alien.bmp')
        self.rect = self.image.get_rect()

        #외계인을 화면 좌측 상단에 배치합니다
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #외계인의 정확한 가로 위치를 저장합니다
        self.x = float(self.rect.x)
    
    def check_edges(self):
        """외계인이 화면 경계에 닿으면 True를 반환합니다"""
        screen_rect = self.screen.get_rect()

        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
    
    def update(self):
        """외계인을 오른쪽으로 움직입니다"""
        self.x += (self.settings.alien_speed *
                    self.settings.fleet_direction)
        self.rect.x = self.x