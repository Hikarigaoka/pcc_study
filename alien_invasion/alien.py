import pygame
import os
import math
import random
from pygame.sprite import Sprite

class Alien(Sprite):
    """함대에 속한 외계인 하나를 담당하는 클래스"""

    def __init__(self, ai_game, wave_number=1):
        """외계인을 초기화하고 시작 위치를 정합니다"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.wave_number = wave_number

        #외계인 이미지를 불러오고 rect 속성을 설정합니다
        current_path = os.path.dirname(__file__)
        image_path = os.path.join(current_path, 'images', 'alien.bmp')
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()

        #외계인을 화면 좌측 상단에 배치합니다
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #외계인의 정확한 가로 위치를 저장합니다
        self.x = float(self.rect.x)
        self.initial_y = float(self.rect.y)
        
        # 급강하 관련 변수
        self.diving = False
        self.dive_speed_x = 0
        self.dive_speed_y = 0
    
    def check_edges(self):
        """외계인이 화면 경계에 닿으면 True를 반환합니다"""
        screen_rect = self.screen.get_rect()
        
        # 회전 반경을 고려하여 여유 공간을 둡니다
        radius = 20 + (self.wave_number - 1) * 10
        margin = radius + self.rect.width / 2

        if self.x >= screen_rect.right - margin or self.x <= margin:
            return True
    
    def update(self):
        """외계인을 오른쪽으로 움직입니다"""
        self.x += (self.settings.alien_speed *
                    self.settings.fleet_direction)
        self.rect.x = self.x
        
        self.rect.x = self.x
        
        self.rect.x = self.x
        
        # S자 움직임 (Sine wave)
        amplitude = 20 + (self.wave_number - 1) * 10  # 웨이브마다 진폭 증가
        frequency = 0.02 + (self.wave_number - 1) * 0.01 # 웨이브마다 주기 변화
        self.rect.y = self.initial_y + amplitude * math.sin(frequency * self.x)
        
        # 급강하 로직
        if not self.diving:
            # 0.1% 확률로 급강하 시작
            if random.random() < 0.001:
                self.diving = True
                self.dive_speed_y = 3 + self.wave_number * 0.5
                # 화면 중앙 쪽으로 약간 이동하도록 X 속도 설정 (단순화)
                if self.rect.x < self.screen.get_rect().centerx:
                    self.dive_speed_x = 1
                else:
                    self.dive_speed_x = -1
        else:
            # 급강하 중일 때는 기존 위치 계산을 무시하고 별도로 이동
            self.rect.y += self.dive_speed_y
            self.rect.x += self.dive_speed_x
            
            # 화면 아래로 벗어나면 제거 (또는 재배치)
            if self.rect.top > self.screen.get_rect().bottom:
                self.kill() # 일단 제거 처리