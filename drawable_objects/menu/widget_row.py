import pygame

from drawable_objects.base import AbstractObject
from drawable_objects.menu.button import Button
from geometry.point import Point
from geometry.rectangle import tuple_to_rectangle, rectangle_to_rect


class WidgetRow(AbstractObject):
    """
    Класс для выравнивания нескольких виджетов в одну строку по центру
    Виджет - объект с полем geometry

    :param scene: сцена, на которой кнопка находится
    :param controller: контроллер
    :param offset: высота по y для выравнивания
    :param widget_offset: промежуток между виджетами (что бы они не слипались)
    """
    BUTTON_DEF_SIZE = [250, 100]

    def __init__(self, scene, controller, offset, widget_offset=0):
        super().__init__(scene, controller)
        self.offset = offset
        self.pos = self.get_base_pos()
        self.widget_offset = widget_offset
        self.widgets = []

    def get_base_pos(self):
        """
        расчитывает базовую точку для группы виджетов
        """
        return Point(
            self.scene.game.width * 0.5,
            self.offset
        )

    def recalc_pos(self):
        """
        Перерасчет позиций виджетов для выравнивания по центру (относительно оффсета)
        """
        newpos = self.get_base_pos()
        if newpos != self.pos:
            self.move(newpos - self.pos)
            self.pos = newpos

    def move(self, movement):
        """
        Передвигает все виджеты параллельным переносом на заданный вектор.

        :param movement: вектор переноса
        """
        for widget in self.widgets:
            widget.move(movement)

    def get_actual_pos(self):
        """
        Получение точки для верхней границы нового виджета

        :return: точка верхней границы нового виджета
        """
        if self.widgets:
            last = self.widgets[-1].geometry
            return Point(last.right + self.widget_offset, last.center.y)
        return self.pos

    def add_button(self, text, function, kwargs={}, size=None):
        """
        Добавляет кнопку в отображаемые виджеты

        :param size: точка, состаящия из высоты(x) и ширины(y) кнопки
        :param text: текст для кнопки
        :param function: вызываемая кнопкой при нажатии на неё функция
        :param kwargs: аргументы вызываемой функции
        """
        if not size:
            size = Point(*WidgetRow.BUTTON_DEF_SIZE)
        pos = self.get_actual_pos()
        geometry = (pos.x, pos.y - size.y / 2,
                    pos.x + size.x, pos.y + size.y / 2)
        btn = Button(self.scene, self.controller,
                     geometry, text, function, kwargs)
        self.widgets.append(btn)
        shift = size.x
        if len(self.widgets) != 1:
            shift += self.widget_offset
        else:
            self.offset += size.y / 2
        shift /= 2
        self.move(Point(-shift, 0))
        self.recalc_pos()

    @property
    def geometry(self):
        top = [i.geometry.top for i in self.widgets]
        bottom = [i.geometry.bottom for i in self.widgets]
        left = [i.geometry.left for i in self.widgets]
        right = [i.geometry.right for i in self.widgets]
        return tuple_to_rectangle((
            min(left), min(top),
            max(right), max(bottom)
        ))


    def update_offset(self, offset):
        """
        Изменение оффсета для отображения группы виджетов

        :param offset: новоый оффсет
        """
        self.offset = Point(*offset)
        self.recalc_pos()

    def process_logic(self):
        for widget in self.widgets:
            widget.process_logic()

    def process_draw(self):
        for widget in self.widgets:
            widget.process_draw()