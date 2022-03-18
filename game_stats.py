import game_functions as gf

class GameStats():
    '''Отслеживание статистики для игры Инопланетные захватчики'''

    def __init__(self, ai_settings):
        '''Инициализирует статистику'''
        self.ai_settings = ai_settings
        self.reset_stats()              # на все время игры будет создаватся один экземпляр данного класса, но часть статистики должна сбрасыватся в начале каждой новой игры. Для этого болльшая часть статистики будет нициализироваться в методе rest_stats вместо init
        self.game_active = False        # игра запускается в неактивном состоянии

        self.high_score = 0            # рекорд игры


    def reset_stats(self):
        '''Инициализирует статистику, изменяющуюся в ходе игры'''
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1

