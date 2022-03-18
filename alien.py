import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    '''Класс, представляющий одного пришельца'''

    def __init__(self, ai_settings, screen):
        '''Инициализирует пришельца и задает его начальную позицию'''
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # загрузка пришельца и назначение атрибута rect
        self.image = pygame.image.load('images/alien.png')
        self.rect = self.image.get_rect()

        # каждый новый пришелец появляется в левом верхнем углу экрана
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # сохранение точной позиции пришельца
        self.x = float(self.rect.x)

    def check_edges(self):
        # возвращает True, если пришелец находится у края экрана
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:        # атрибут right у атрибута rect пришельца больше чем атрибут right у экрана
            return True
        elif self.rect.left <= 0:                       # для левого края
            return True

    def update(self):
        '''Перемещает пришельца вправо'''
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x
