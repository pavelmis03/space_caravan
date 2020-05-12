import pygame

from constants.color import COLOR
from drawable_objects.base import DrawableObject
from drawable_objects.text import Text
from geometry.point import Point
from geometry.rectangle import tuple_to_rectangle, rectangle_to_rect, get_rectangle_copy


class CheckBox(DrawableObject):
    """
    Класс чекбокса для настроек
    BG_COLOR - цвет фона чекбокса
    BG_ENABLED_COLOR - цвет внутреннего квадратика чекбокса
    TEXT_COLOR - текст цвета
    FONT_NAME - шрифт, используемый для отображения цвета
    SIZE - коэфиицент, отвечающий за то, насколько должен
    заполнять внутренний квадрат внешний (1/2 - половина)
    """
    BG_COLOR = (120, 120, 120)
    BG_ENABLED_COLOR = (220, 220, 220)
    TEXT_COLOR = COLOR['WHITE']
    FONT_NAME = 'Consolas'
    SIZE = 5 / 8

    def __init__(self, scene, cotroller, geometry, label='Test', font_size=16, enabled=False):
        self.geometry = tuple_to_rectangle(geometry)
        super().__init__(scene, cotroller, self.geometry.center)
        self.label = Text(scene, self.geometry.center, label,
                         CheckBox.TEXT_COLOR, 'left', CheckBox.FONT_NAME, font_size, False)
        # move label to left edge of checkbox:
        self.label.pos.x += self.geometry.width / 2
        self.label.pos.y -= self.label.text_surface.get_height() / 2
        # set up second geometry for enabled square(check):
        self.c_geometry = get_rectangle_copy(self.geometry)
        self.c_geometry.size *= CheckBox.SIZE

        self.check = enabled

    def move(self, movement):
        """
        Передвигает чекбокс параллельным переносом на заданный вектор.

        :param movement: вектор переноса
        """
        self.geometry.move(movement)
        self.label.pos = self.geometry.center

    def process_logic(self):
        click_pos = self.controller.get_click_pos()
        if click_pos and self.geometry.is_inside(click_pos):
            self.check = not self.check

    def process_draw(self):
        pygame.draw.rect(self.scene.screen, CheckBox.BG_COLOR, rectangle_to_rect(self.geometry))
        if self.check:
            pygame.draw.rect(self.scene.screen, CheckBox.BG_ENABLED_COLOR, rectangle_to_rect(self.c_geometry))
        self.label.process_draw()