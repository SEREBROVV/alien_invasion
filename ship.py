import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        '''Инициализирует корабль и задает его начальную позицию'''
        super(Ship, self).__init__()      # теперь данный класс наследуется от Sprite
        self.screen = screen
        self.ai_settings = ai_settings

        # загрузка изображения корабля и получения прямоугольника
        self.image = pygame.image.load('images/ship.png')   # возвращает поверхность, представляющую корабль
        self.rect = self.image.get_rect()   # делает из корабля произвольной формы - прямоугольник
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx    # атрибуту (координата х центра коробля) присваивается значение атрибута (координата центра экрана)
        self.rect.bottom = self.screen_rect.bottom      # атрибуту (координата y низа коробля) присваивается значение атрибута bottom (y низ) экрана

        self.center = float(self.rect.centerx)

        self.moving_right = False           # флаг который равен False когда клавиша не нажата и True когда нажата
        self.moving_left = False

    def update(self):
        '''Обновляет позицию игрока с учетом флага'''
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        self.rect.centerx = self.center     # обновление атрибута rect на основании self.center, сюда будет сохранена только целая часть self.center

    def blitme(self):
        '''Рисует корабль в текущей позиции'''
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        '''Размещает корабль в центре нижней стороны'''
        self.center = self.screen_rect.centerx