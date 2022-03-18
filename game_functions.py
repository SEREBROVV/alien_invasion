import sys      # данный модуль завершает игру по команде игрока
import pygame
from random import randint
from time import sleep

from bullet import Bullet
from alien import Alien
from star import Star

def check_keydown_events(event, ai_settings, screen, stats, ship, aliens, bullets):      # отслеживает когда клавиша нажата
    if event.key == pygame.K_RIGHT:  # проверяет атрибут event.key совпадает ли он с клавишей K_RIGHT
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_p:
        stats_game_p(ai_settings, screen, stats, ship, aliens, bullets)

def fire_bullet(ai_settings, screen, ship, bullets):
    # создание новой пули и ключение её в группу bullets
    if len(bullets) <= ai_settings.bullet_allowed:  # ограничение количества пуль на экране
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def check_keyup_events(event, ship):    # отслеживает когда клавиша отпущена
    if event.key == pygame.K_RIGHT:  # показывает что надо делать когда отпущена клавиша K_RIGHT
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    '''Обрабатывает нажатия клавиш и события мыши'''
    for event in pygame.event.get():    # данный метод необходим для получения доступа к событиям
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, ship, aliens, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()           # возвращает кортеж с координатами x и y точки щелчка
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)
        elif event.type == pygame.K_p:
            check_keydown_events(event, ai_settings, screen, stats, ship, aliens, bullets)

def stats_game_p(ai_settings, screen, stats, ship, aliens, bullets):
    if not stats.game_active:
        #сброс игровых настроек
        ai_settings.initialize_dynamic_settings()
        #указатель миши скрывается
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True

        # очистка списков пришельцев и пуль
        aliens.empty()
        bullets.empty()

        # создание нового флота и размещение корабля в центре
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    '''Запускает игру при нажатии кнопки Play'''
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)         # метод collidepoint проверяет находится ли точка щелчка в пределах области, определяемой прямоугольником кнопки Play
    if button_clicked and not stats.game_active:            # флаг button_clicked содержит значения True или False, игра запускается если пользователь нажал на play и игра была не активна
        # сброс игровых настроек
        ai_settings.initialize_dynamic_settings()
        # указатель миши скрывается
        pygame.mouse.set_visible(False)         # set_visible() со значение False приказывает Pygame скрыть указатель, когда он находится над окном игры
        # сброс игровой статистики
        stats.reset_stats()
        stats.game_active = True

        # сброс изображений счетов и уровней, и оставшихся попыток
        sb.prep_score()
        sb.prep_level()
        sb.prep_ships()

        # очистка списков пришельцев и пуль
        aliens.empty()
        bullets.empty()

        # создание нового флота и размещение корабля в центре
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
def check_high_score(stats, sb):
    '''Проверяет появился ли новый рекорд'''
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, stars, play_button):
    '''Обновляет изображения на экране и отображает новый экран'''
    screen.fill(ai_settings.bg_color)  # при каждом проходе цикла перерисовывается экран
    # все пули выводятся позади изображений коробля и пришельцев
    for bullet in bullets.sprites():        # метод возвращает список всех спрайтов в группе
        bullet.draw_bullet()
    ship.blitme()
    stars.draw(screen)
    aliens.draw(screen)         # когда вызывается этот метод для группы Pygame атоматически выводит каждый элемент группы в позиции, определяемой его атрибутом rect

    sb.show_score()

    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()  # приказывает отобразить последний отрисованный экран. При каждом выполнении цикла while
                           # будет отображатся новый экран(поверхность) уже с новыми позициями объектов

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''Обработка коллизий пуль с пришельцами'''
    # Проверка попаданий в пришельцев
    # При обнаружении попадания удалить пулю и пришельца
    collisions = pygame.sprite.groupcollide(bullets, aliens, True,
                                            True)  # перебирает все пули в группе и всех пришельцев в группе. Каждый раз когда между прямоугольником пули и пришельца обнаруживается перекрытие, groupcollide() добавляет пары ключ-значение в возвращаемый словарь. Два аргумента True сообщают нужно ли удалить пули и пришельца после перекрытия

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points*len(aliens)     # подсчет очков за попадания в пришельцев
            sb.prep_score()
            check_high_score(stats, sb)

    if len(aliens) == 0:
        # уничтожение существующих пуль и создание нового флота
        bullets.empty()
        ai_settings.increase_speed()
        # увеличение уровня
        stats.level += 1
        sb.prep_level()     # создание изображения из обновленного уровня
        create_fleet(ai_settings, screen, ship, aliens)

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''Обновляет позиции пуль и удаляет старые пули'''
    bullets.update()            # приводит к автоматическому вызову update для каждого спрайта в группе

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)

def get_number_aliens_x(ai_settings, alien_width):
    '''Считает кол-во пришельцев в ряду'''
    available_space_x = ai_settings.screen_width - 2 * alien_width      # доступное пространство для пришельцев по х
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_hight):
    '''Считатет количество пришельцев по вертикали'''
    available_space_y = ai_settings.screen_height - 3 * alien_hight - ship_height       # доступное вертикальное пр-во
    number_rows = int(available_space_y / (2*alien_hight))
    return number_rows

def get_number_stars(ai_settings, star_width, star_height):
    '''Считает количество звезд'''
    number_stars_x = int((ai_settings.screen_width - 2 * star_width) / (2 * star_width))
    number_stars_y = int((ai_settings.screen_height -  2 *  star_height) / (4 * star_height))
    return [number_stars_x, number_stars_y]

def create_star(ai_settings, screen, stars, number_stars_x, number_stars_y):
    '''Создает звезду и добавляет её в группу'''
    random_number = randint(-10, 10)
    star = Star(ai_settings, screen)
    star_width = star.rect.width
    star.x = star_width + random_number * number_stars_x * star.rect.width
    star.rect.x = star.x
    star.rect.y = star.rect.height + random_number * number_stars_y * star.rect.height
    stars.add(star)

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    '''Создает пришельца и раземещает его вряду'''
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width      # ширина пришельца
    alien.x = alien_width + 2 * alien_width * alien_number      # позиция пришельца по x
    alien.rect.x = alien.x              # alien.x использует только потому что это float, сделано для более точного метсонахождения пришельца
    alien.rect.y = 4 * alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_group_stars(ai_settings, screen, stars):
    '''Создает все звезды'''

    star = Star(ai_settings, screen)
    number_stars_x = get_number_stars(ai_settings, star.rect.width, star.rect.height)[0]
    number_stars_y = get_number_stars(ai_settings, star.rect.width, star.rect.height)[1]
    for y in range(number_stars_y):
        for x in range(number_stars_x):
             create_star(ai_settings, screen, stars, x, y)


def create_fleet(ai_settings, screen, ship, aliens):
    '''Создает флот пришельцев'''

    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # Создание первого ряда пришельцев
    for row_number in range(number_rows - 3):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def check_fleet_edges(ai_settings, aliens):
    '''Реагирует на достижение пришельцем края экрана'''
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    '''Опускает флот и меняет направление флота'''
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def change_fleet_drop(ai_settings, stars):
    '''Опускает капли'''
    for drop in stars.sprites():
        drop.rect.y += ai_settings.fleet_star_speed

def create_new_stars(ai_settings, screen, stars):
    '''Делает новый ряд каплей, когда старый спустился'''
    for star in stars.sprites():
        if star.check_placedown_star(ai_settings):
            star.rect.y -= ai_settings.screen_height

def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
    '''Обрабатывает столкновения коробля с пришельцем'''
    if stats.ships_left > 0:
        stats.ships_left -= 1

        # обновление игровой информации
        sb.prep_ships()

        aliens.empty()
        bullets.empty()

        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # пауза
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)          # указатель свнова становится видимым, когда игра заканчивается

def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets):
    '''Проверяет добрались ли пришельцы до нижнего края экрана'''
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
            break

def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets):
    '''Проверяет достиг ли флот края экрана, после чего обновляет позиции всех пришельцев во флоте'''
    check_fleet_edges(ai_settings, aliens)
    aliens.update()         # мы используем метод update для группы aliens, что приводит к автоматическому вызову метода update для каждого пришельца

    # Проверка коллизий "пришелец-корабль"
    if pygame.sprite.spritecollideany(ship, aliens):        # получает два аргумента спрайт и группу и пытается найти любой элемент группы, вступивший в коллизию со спрайтом и останавливает цикл после обнаружении столкнувшегося элемента. Если ни одна коллизия не обнаружена метод возращает None
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
    # проверка пришельцев, добравшихся до нижнего края экрана
    check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets)