import pygame

from drawable_objects.base import DrawableObject
from geometry.point import Point
from geometry.rectangle import Rectangle, rect_to_rectangle, rectangle_to_rect


class AlignmentStrategy:
    """
    Базовый класс стратегии выравнивания текста.
    """

    def execute(self, rectangle, pos):
        """
        Исполнить стратегию.

        :param rectangle: прямоугольник поверхности текста
        :param pos: выравнивающая точка
        """
        pass


class StrategyLeft(AlignmentStrategy):
    """
    Выравнивание по левому верхнему углу.
    """

    def execute(self, rectangle, pos):
        rectangle.top_left = pos


class StrategyCenter(AlignmentStrategy):
    """
    Выравнивание по центру.
    """

    def execute(self, rectangle, pos):
        rectangle.center = pos


class Text(DrawableObject):
    """
    Надпись на экране игры.
    Не умеет работать с строками со \n
    Для текста с переносами строки см. класс MultilineText

    :param scene: сцена, на которой находится текст
    :param pos: точка, по которой текст выравнивается
    :param text: строка текста
    :param: color: цвет текста
    :param align: выравнивание; пока поддерживается только 2 выравнивания: 'left' (pos - левый верхний угол надписи)
        и 'center' (pos - центр надписи)
    :param font_name: название шрифта
    :param font_size: размер шрифта
    :param is_bold: полужирный ли шрифт
    :param is_italic: наклонный ли шрифт
    """
    ALIGNS = {
        'left': StrategyLeft(),
        'center': StrategyCenter(),
    }

    def __init__(self, scene, pos, text='Define me!', color=(255, 255, 255), align='left', font_name='Comic Sans',
                 font_size=35, is_bold=True, is_italic=False, width_limit=None):
        super().__init__(scene, None, pos)
        self.color = color
        if align in Text.ALIGNS:
            self.align = align
        else:
            self.align = 'left'
        self.font = pygame.font.SysFont(
            font_name, font_size, is_bold, is_italic)
        self.text = None
        self.text_surface = None
        self.width_limit = width_limit
        self.update_text(text)

    def update_text(self, text):
        """
        Изменение надписи. Поддерживается изменение строки текста без изменения остальных параметров объекта.

        :param text: новая строка текста
        """
        self.text = text
        self.text_surface = self.font.render(self.text, True, self.color)
        if self.width_limit:
            rect = self.text_surface.get_rect()
            if rect.width > self.width_limit:
                x = rect.width - self.width_limit
                self.text_surface = self.text_surface.subsurface(
                    (x, rect.y, rect.width - x, rect.height))
        self.rect = rect_to_rectangle(self.text_surface.get_rect())

    def process_draw(self):
        rectangle = self.rect
        if self.align in Text.ALIGNS:
            Text.ALIGNS[self.align].execute(rectangle, self.pos)
        self.scene.screen.blit(self.text_surface, rectangle_to_rect(rectangle))
