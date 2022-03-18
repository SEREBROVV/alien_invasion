import pygame

from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
    # Инициализирует игру, settings и объект экрана
    pygame.init()       # инициализирует настройки, необходимые Pygame для нормальной работы
    ai_settings = Settings()    # ai потому что Alien Invasion
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))       # создаёт экран игру, кортеж из кол-ва пикселей
    pygame.display.set_caption('Иноплонетные захватчики')
    ship = Ship(ai_settings, screen)     # создание корабля
    stats = GameStats(ai_settings)
    play_button = Button(ai_settings, screen, 'Play')
    sb = Scoreboard(ai_settings, screen, stats)

    # Создание группы для хранения пуль
    bullets = Group()       # чтобы хранить пули в группе
    aliens = Group()        # группа для хранения всех пришельцев в игре
    stars = Group()

    # Создание флота пришельцев
    gf.create_group_stars(ai_settings, screen, stars)
    gf.create_fleet(ai_settings, screen, ship, aliens)


# основной цикл программы
    while True:
        gf.check_events(ai_settings, screen, stats, sb,  play_button, ship, aliens, bullets)
        if stats.game_active:                                   # то что в if должно выполнятся, только когда игра активна, всё что не в if должно выполнятся всегда
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.change_fleet_drop(ai_settings, stars)
            gf.create_new_stars(ai_settings, screen, stars)
            gf.update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets)
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, stars, play_button)

run_game()






