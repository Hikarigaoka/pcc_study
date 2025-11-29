import pygame
import random

class Starfield:
    def __init__(self, game):
        self.screen = game.screen
        self.settings = game.settings
        self.stars = []
        for _ in range(100):
            self.stars.append([random.randint(0, self.settings.screen_width), random.randint(0, self.settings.screen_height)])
            
    def update(self):
        for star in self.stars:
            star[1] += 2
            if star[1] > self.settings.screen_height:
                star[1] = 0
                star[0] = random.randint(0, self.settings.screen_width)
                
    def draw(self):
        for star in self.stars:
            pygame.draw.circle(self.screen, (150, 150, 150), star, 2)
