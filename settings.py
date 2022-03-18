class Settings():
    """Класс для хранения всех настроек игры Инопланетное вторжение"""

    def __init__(self):
        """Инициализируем настройки игры"""
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.ship_speed_factor = 1.5        # скорость коробля, добавлена для повышения точности управления скоростью. Теперь корабль смещается на 1.5 пикселя. Дробные значения скорости позволяют лучше управлять скоростью коробля при повышении темпа игры.
        self.ship_limit = 3

        # настройки пришельцев
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 25
        self.fleet_direction = 1            # обозначает движение вправо, а -1 влево

        # настройки звезды
        self.fleet_star_speed = 1

        #параметры пули
        self.bullet_speed_factor = 2
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullet_allowed = 3

        # Темп ускорения игры
        self.speedup_scale = 1.5

        # Темп роста стоимости пришельцев
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        '''Инициализирует настройки, изменяющиеся в ходе игры'''
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 2
        self.alien_speed_factor = 1

        self.fleet_direction = 1

        # подсчет очков
        self.alien_points = 50

    def increase_speed(self):
        '''Увеличивает настройки скорости'''
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points*self.score_scale)