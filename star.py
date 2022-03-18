import pygame
from pygame.sprite import Sprite

class Star(Sprite):
    '''Делает звёздочки'''
    def __init__(self, ai_settings, screen):
        super(Star, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        self.image = pygame.image.load('images/drop.png')
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def check_placedown_star(self, ai_settings):
        screen_rect = self.screen.get_rect()
        if self.rect.y >= screen_rect.bottom:
            return True

