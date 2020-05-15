import pygame

from constants.color import COLOR
from drawable_objects.base import DrawableObject
from drawable_objects.text import Text
from geometry.point import Point
from geometry.rectangle import tuple_to_rectangle, rectangle_to_rect, get_rectangle_copy, rect_to_rectangle, Rectangle


class CheckBox(DrawableObject):
    """
    Класс чекбокса для настроек
    BG_COLOR - цвет фона чекбокса
    BG_ENABLED_COLOR - цвет внутреннего квадратика чекбокса
    TEXT_COLOR - текст цвета
    FONT_NAME - шрифт, используемый для отображения цвета
    SIZE - коэфиицент, отвечающий за то, насколько должен
    заполнять внутренний квадрат внешний (1/2 - половина)

    self.select - квадратик
    self.selected - внутреннее выделение квадратика
    self.geometry - все вмете (текст тоже)
    """
    BG_COLOR = (120, 120, 120)
    BG_ENABLED_COLOR = (220, 220, 220)
    TEXT_COLOR = COLOR['WHITE']
    FONT_NAME = 'Consolas'
    SIZE = 3 / 5

    def __init__(self, scene, cotroller, pos, size=10, label='Test', font_size=16, align='left', enabled=False):
        self.select = tuple_to_rectangle((0, 0, size, size))
        super().__init__(scene, cotroller, self.select.center)
        self.label = Text(scene, self.select.center, label,
                          CheckBox.TEXT_COLOR, 'left', CheckBox.FONT_NAME, font_size, False)
        self.align = align
        self.set_up_size()
        self.move_to(pos)
        self.check = enabled

    def move(self, movement):
        """
        Передвигает чекбокс параллельным переносом на заданный вектор.
        Учитывает при переносе align

        :param movement: вектор переноса
        """
        self.geometry.move(movement)
        self.select.move(movement)
        self.selected.move(movement)
        self.label.pos += movement

    def move_to(self, position):
        """
        Передвигает чекбокс в определенную позицию
        :param position: новая позиция
        """
        movement = position - self.geometry.top_left
        if self.align == 'center':
            half_w = (self.select.width + self.label.text_surface.get_width()) / 2
            movement.x -= half_w
        self.move(movement)

    def set_up_size(self):
        """
        Инициализация полей и относительных расположений чекбокса
        """
        self.label.pos = self.select.center * 1
        self.label.pos.x += 3 # little space between box and test
        # move label to left edge of the checkbox:
        self.label.pos.x += self.select.width / 2
        self.label.pos.y -= self.label.text_surface.get_height() / 2
        # set up second geometry for enabled square(check):
        self.selected = get_rectangle_copy(self.select)
        self.selected.size *= CheckBox.SIZE
        # set up hitbox geometry
        self.geometry = Rectangle(self.select.left, self.select.top,
                                  self.label.pos.x + self.label.rect.right, self.select.bottom)

    def process_logic(self):
        click_pos = self.controller.get_click_pos()
        if click_pos and self.geometry.is_inside(click_pos):
            self.check = not self.check

    def process_draw(self):
        pygame.draw.rect(self.scene.screen, CheckBox.BG_COLOR, rectangle_to_rect(self.select))
        if self.check:
            pygame.draw.rect(self.scene.screen, CheckBox.BG_ENABLED_COLOR, rectangle_to_rect(self.selected))
        self.label.process_draw()
        # pygame.draw.rect(self.scene.screen, (255, 0, 0), rectangle_to_rect(self.geometry), 2)