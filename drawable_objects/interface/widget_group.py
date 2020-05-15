import pygame

from constants.color import COLOR
from drawable_objects.base import AbstractObject
from drawable_objects.button import Button
from drawable_objects.checkbox import CheckBox
from drawable_objects.multiline_text import MultilineText
from geometry.point import Point
from geometry.rectangle import tuple_to_rectangle


class WidgetGroup(AbstractObject):
    """
    Класс для динамического выравнивания виджетов по центру
    На данный момент виджеты - это кнопки(Button) и чекбоксы(CheckBox)
    У виджета должно быть поле geometry

    :param scene: сцена, на которой кнопка находится
    :param controller: контроллер
    :param offset: оффсет центра в процентах [(0-1), (0-1)] относительно размеров окна
    :param widget_geometry: размеры создаваемых виджетов (базовый)
    :param widget_offset: расстояние между виджетами (что бы они не слипались)
    """

    BUTTON_DEF_SIZE = [150, 60]
    CHECKBOX_DEF_SIZE = 20

    def __init__(self, scene, controller, offset, widget_offset=0):
        super().__init__(scene, controller)
        self.offset = Point(*offset)
        self.pos = self.get_base_pos()
        self.widget_offset = widget_offset
        self.widgets = []

    def get_base_pos(self):
        """
        расчитывает базовую точку для группы виджетов
        """
        return Point(
            self.scene.game.width * self.offset.x,
            self.scene.game.height * self.offset.y
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
        :return точка верхней границы нового виджета
        """
        if self.widgets:
            last = self.widgets[-1].geometry
            return Point(last.center.x, last.bottom + self.widget_offset)
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
            size = Point(*WidgetGroup.BUTTON_DEF_SIZE)
        pos = self.get_actual_pos()
        geometry = (pos.x - size.x / 2, pos.y, pos.x + size.x / 2, pos.y + size.y)
        btn = Button(self.scene, self.controller,
                     geometry, text, function, kwargs)
        self.widgets.append(btn)

    def add_checkbox(self, text, size=None):
        """
        Добавляет чекбокс в отображаемые виджеты
        :param text: Текст для чекбокса
        :param size: Размеры чекбокса (самого квадрата)
        """
        if not size:
            size = WidgetGroup.CHECKBOX_DEF_SIZE
        pos = self.get_actual_pos()
        pos.y += size / 2
        p = self.get_actual_pos()
        box = CheckBox(self.scene, self.controller,
                       pos, size, text, align='center')
        self.widgets.append(box)

    def add_multilinetext(self, text, **text_kwargs):
        """
        Добавляет многострочный текст в отображаемые виджеты
        :param text: многострочный текст
        :param text_kwargs: аргументы многострочного текста
        """
        pos = self.get_actual_pos()
        label = MultilineText(self.scene, Point(0, 0), text, **text_kwargs)
        label.move(pos)
        self.widgets.append(label)

    def update_offset(self, offset):
        """
        Изменение оффсета для отображения группы виджетов
        :param offset: новоый оффсет
        """
        self.offset = Point(*offset)
        self.recalc_pos()

    def process_logic(self):
        self.recalc_pos()
        for widget in self.widgets:
            widget.process_logic()

    def process_draw(self):
        for widget in self.widgets:
            widget.process_draw()
