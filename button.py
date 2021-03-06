import pygame.font      # позволяет Pygame выводить текст на экран

class Button():

    def __init__(self, ai_settings, screen, msg):
        '''Инициализирует атрибуты кнопки'''
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # назвачение размеров и свойств кнопки
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)       # подготовка атрибута font для вывода текста. Аргумент None сообщает, что должен использоваться шрифт текста по умолчанию, 48 - размер текста


        # Построение объкта rect кнопки и выравнивание по центру экрана
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # Сообщение кнопки создается только один раз
        self.prep_msg(msg)

    def prep_msg(self, msg):
        '''Преобразует msg в прямоугольник и выравнивает текст по центру'''
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)    # font.render преобразует текст msg в изображение. True означает, что включен режин сглаживание текста. Потом передается цвет изображения и цвет фона
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center       # выравнивает изображения текста по центру кнопки

    def draw_button(self):
        '''Отображение пустой кнопки и вывод сообщение'''
        self.screen.fill(self.button_color, self.rect)          # рисует прямоугольную часть кнопки
        self.screen.blit(self.msg_image, self.msg_image_rect)   # выводит изображение текста на экран с передачей изображения и объекта rect, связанного с изображением
