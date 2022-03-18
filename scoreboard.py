import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard():
    '''Класс для вывода информации о рекорде игры'''
    def __init__(self, ai_settings, screen, stats):
        '''Инициализирует атрибуты подсчета очков'''
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # Настройки шрифта для вывода счета
        self.text_color = (30, 30, 30)
        self.font =  pygame.font.SysFont(None, 48)
        # подготовка изображений счетов
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        '''Преобразует текущий счет в графическое изображение'''
        rounded_score = int(round(self.stats.score, -1))        # функция round округляет дробное число до заданного кол-ва знаков, переданного во втором аргументе. Если он равен отрицательному числу, round() округляет значение до ближайших десятков, сотен и т.д.
        score_str = "{:,}".format(rounded_score)                # директива форматирования строки приказывает Python вставить запятые при преобразования числового значения в строку
        self.score_image = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color)    # создает изображение из текста с счетом игры

        # вывод счета в правой верхней части экрана
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = self.screen_rect.top       # верхняя граница изображения счета снижается на 20 пикселей от начала экрана

    def prep_high_score(self):
        '''Преобразует рекордный счет в графическое изображение'''
        high_score = int(round(self.stats.score, -1))
        high_score_str = "{:,}".format(high_score)

        self.high_score_image = self.font.render(high_score_str, True, self.text_color,
                                            self.ai_settings.bg_color)
        # выравниватся по центру верхней стороны
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.score_rect.top = self.screen_rect.top

    def prep_level(self):
        '''Преобразует уровень в графическое изображение'''
        self.level_image = self.font.render(str(self.stats.level), True, self.text_color, self.ai_settings.bg_color)    # создает изображение на базе значения, хранящегося в stats.level

        # уровень выводится под текущим счетом
        self.level_rect = self.level_image.get_rect()
        self.level_rect.centerx = self.score_rect.centerx
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        '''Сообщает количество оставшихся кораблей'''
        self.ships = Group()                                    # создает пустую группу для хранения экземпляров кораблей
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)                                # после всех введённых параметров для созданного корабля он добавляется в группу

    def show_score(self):
            '''Выводит счет, рекорд и уровень на экран'''
            self.screen.blit(self.score_image, self.score_rect)     # метод выводит изображение счета в позиции, определяемой score_rect
            self.screen.blit(self.high_score_image, self.high_score_rect)       # тоже самое для глобального рекорда
            self.screen.blit(self.level_image, self.level_rect)
            # вывод кораблей
            self.ships.draw(self.screen)            # мы вызываем метод draw для группы, а Pygame рисует каждый отдельный корабль