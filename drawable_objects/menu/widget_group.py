import pygame

from drawable_objects.base import AbstractObject
from drawable_objects.menu.button import Button
from drawable_objects.menu.checkbox import CheckBox
from drawable_objects.menu.list_widget import ListWidget
from drawable_objects.menu.multiline_text import MultilineText
from drawable_objects.menu.text import Text
from drawable_objects.menu.textbox import TextBox
from drawable_objects.menu.widget_row import WidgetRow
from geometry.point import Point
from geometry.rectangle import rectangle_to_rect


class WidgetGroup(AbstractObject):
    """
    Класс для динамического выравнивания виджетов по центру
    Виджет - объект с полем geometry

    :param scene: сцена, на которой кнопка находится
    :param controller: контроллер
    :param offset: оффсет центра в процентах [(0-1), (0-1)] относительно размеров окна
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

        :return: точка верхней границы нового виджета
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
        geometry = (pos.x - size.x / 2, pos.y,
                    pos.x + size.x / 2, pos.y + size.y)
        btn = Button(self.scene, self.controller,
                     geometry, text, function, kwargs)
        self.widgets.append(btn)

    def add_checkbox(self, text, size=None) -> CheckBox:
        """
        Добавляет чекбокс в отображаемые виджеты

        :param text: Текст для чекбокса
        :param size: Размеры чекбокса (самого квадрата)
        :return: ссылка на созданный checkbox
        """
        if not size:
            size = WidgetGroup.CHECKBOX_DEF_SIZE
        pos = self.get_actual_pos()
        pos.y += size / 2
        box = CheckBox(self.scene, self.controller,
                       pos, size, text, align='center')
        self.widgets.append(box)
        return box

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

    def add_textbox(self, size, prompt_str):
        """
        Добавляет текстбокс в отображаемые объекты
        :param size: Point с указанием размеров
        :param prompt_str: строка подсказки
        """
        pos = self.get_actual_pos()
        geom = (pos.x - size.x/2, pos.y + self.widget_offset,
                pos.x + size.x/2, pos.y + self.widget_offset + size.y)
        textbox = TextBox(self.scene, self.controller, geom, prompt_str)
        self.widgets.append(textbox)

    def add_list_widget(self, size, item_height, elements):
        """
        Добавляет список миров в отображаемые объекты
        :param size: Point с размерами списка
        :param item_height: высота элемента списка
        :param elements: список элементов
        """
        pos = self.get_actual_pos()
        size /= 2
        geom = (pos.x - size.x, pos.y - size.y,
                pos.x + size.x, pos.y + size.y)
        list_widget = ListWidget(self.scene, self.controller, geom, item_height, elements)
        self.widgets.append(list_widget)

    def add_widget_row(self, widget_offset):
        """
        Добавляет строку виджетов в отображаемые объекты
        """
        pos = self.get_actual_pos()
        offset = pos.y
        widgetrow = WidgetRow(self.scene, self.controller, offset, widget_offset)
        self.widgets.append(widgetrow)

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
            # pygame.draw.rect(self.scene.screen, (255, 0, 0), rectangle_to_rect(widget.geometry), 4)
