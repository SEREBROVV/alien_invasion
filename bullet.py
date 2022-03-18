import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    '''Создает объект пули в текущей позиции коробля'''
    def __init__(self, ai_settings, screen, ship):
        super(Bullet, self).__init__()      # класс пули наследуется от класса Sprite, чтобы была возможность работать не с одной пулей, а с множеством пуль
        self.screen = screen

        # создание пули в позиции (0,0) и назначение правильной позиции
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)      # создаётся пули с характеристиками в начальной точке, сейчас мы создаём пулю не на основу изображения, поэтому приходится писать эту строку
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Позиция пули хранится в вещественном формате для внесения более точных изменений в скорость пули
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        '''Перемещает пулю вверх по экрану'''
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        '''Выводит пули на экран'''
        pygame.draw.rect(self.screen, self.color, self.rect)