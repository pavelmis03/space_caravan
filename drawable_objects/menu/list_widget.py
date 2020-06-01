import pygame

from typing import Tuple, List

from scenes.base import Scene
from controller.controller import Controller
from constants.color import COLOR
from drawable_objects.base import DrawableObject
from drawable_objects.menu.text import Text
from geometry.rectangle import Rectangle, tuple_to_rectangle, rectangle_to_rect, intersect
from geometry.point import Point, point_to_tuple


class ListWidgetItem(DrawableObject):
    """
    Пункт списка ListWidget. Выравнивается по родительскому объекту списка самостоятельно. Содержит в себе текст;
    может быть выбран пользователем нажатием мыши.

    :param scene: сцена объекта
    :param controller: контроллер
    :param parent: родительский объект списка
    :param value: значение пункта - отображаемая на нем строка
    """
    TEXT_COLOR = COLOR['BLACK']
    BG_COLOR = COLOR['WHITE']
    BG_CHOSEN_COLOR = COLOR['LIGHT_GREEN']
    FRAME_COLOR = COLOR['BLACK']
    FONT_NAME = 'freesansbold'

    def __init__(self, scene: Scene, controller: Controller, parent, value: str):
        super().__init__(scene, controller, Point())
        self.parent = parent
        self.value = value
        self.geometry = Rectangle(0, 0, 0, self.parent.item_height)
        font_size = self.parent.item_height
        self.text = Text(scene, self.geometry.top_left, value, self.TEXT_COLOR, 'left', self.FONT_NAME, font_size,
                         False, False)
        self.visible_part = None
        self.chosen = False

    def __lt__(self, other):
        return self.value < other.value

    def update_geometry(self, index):
        """
        Обновление размера и положения по родительскому объекту. Вычисление видимой пользователю области объекта.

        :param index: индекс этого пункта в списке
        """
        self.geometry.width = self.parent.geometry.width
        left, top = point_to_tuple(self.parent.geometry.top_left)
        top += self.parent.item_height * index + self.parent.scroll_value
        self.geometry.top_left = Point(left, top)
        self.text.pos = self.geometry.top_left
        self.visible_part = intersect(self.geometry, self.parent.geometry)

    def process_logic(self):
        """
        Логика объекта - отслеживание положения щелчка мыши, чтобы понять, выбран ли пункт.
        """
        click_pos = self.controller.get_click_pos()
        if self.controller.click_pos and self.parent.geometry.is_inside(click_pos):
            self.chosen = self.visible_part.is_strictly_inside(click_pos)

    def process_draw(self):
        """
        Отрисовка объекта. Объект отрисовывается, если виден пользователю. Если виден не полностью, отрисовывается
        видимая область, но без текста.
        """
        if self.visible_part.is_empty():
            return
        bg_color = self.BG_CHOSEN_COLOR if self.chosen else self.BG_COLOR
        pygame.draw.rect(self.scene.screen, bg_color,
                         rectangle_to_rect(self.visible_part))
        if self.geometry.height == self.visible_part.height:
            self.text.process_draw()
        pygame.draw.rect(self.scene.screen, self.FRAME_COLOR,
                         rectangle_to_rect(self.visible_part), 1)


class ListWidget(DrawableObject):
    """
    Список для пользовательского выбора. Пункт выбирается щелчком мыши; список можно прокручивать вверх/вниз.

    :param scene: сцена объекта
    :param controller: контроллер
    :param geometry: кортеж с координатами прямоугольника объекта
    :param item_height: высота каждого пункта в списке
    :param elements: значения пунктов списка
    """
    FRAME_COLOR = (0, 0, 200)
    KEY_UP = pygame.K_UP
    KEY_DOWN = pygame.K_DOWN
    SCROLL_SPEED = 5

    def __init__(self, scene: Scene, controller: Controller, geometry: Tuple, item_height: int, elements: List[str]):
        self.geometry = tuple_to_rectangle(geometry)
        super().__init__(scene, controller, self.geometry.center)
        self.scroll_value = 0
        self.item_height = item_height
        self.items = list()
        for element in elements:
            self.items.append(ListWidgetItem(scene, controller, self, element))
        self.items.sort()
        self.choice = None

    def add_element(self, element: str):
        """
        Добавление в список элемента. Имеет смысл хранить в списке только неповторяющиеся значения.
        """
        self.items.append(ListWidgetItem(self.scene, self.controller, self, element))
        self.items.sort()

    def remove_element(self, element: str):
        for item in self.items:
            if item.value == element:
                self.items.remove(item)

    def get_choice(self):
        return self.choice

    def arrange_items(self):
        index = 0
        for item in self.items:
            item.update_geometry(index)
            index += 1

    def __contains__(self, element):
        """
        Перегрузка оператора in. Позволяет узнать, есть ли в списке пункт с заданным значением.
        """
        for item in self.items:
            if item.value == element:
                return True
        return False

    def scroll_controls(self):
        if self.controller.is_key_pressed(self.KEY_UP):
            self.scroll_value += self.SCROLL_SPEED
        if self.controller.is_key_pressed(self.KEY_DOWN):
            self.scroll_value -= self.SCROLL_SPEED

    def apply_scroll_borders(self):
        """
        Применение границ к текущему значению прокрутки списка. Список не прокручивается наверх за первый элемент
        и вниз за последний.
        """
        self.scroll_value = min(self.scroll_value, 0)
        lower_border = min(0, self.geometry.height -
                           self.item_height * len(self.items))
        self.scroll_value = max(self.scroll_value, lower_border)

    def move(self, movement):
        """
        Перемещение объекта на заданный вектор. Нужно для встраивания в WidgetGroup.
        """
        self.geometry.move(movement)

    def process_logic(self):
        self.scroll_controls()
        self.apply_scroll_borders()
        self.arrange_items()
        self.choice = None
        for item in self.items:
            item.process_logic()
            if item.chosen:
                self.choice = item.value

    def process_draw(self):
        pygame.draw.rect(self.scene.screen, self.FRAME_COLOR,
                         rectangle_to_rect(self.geometry), 10)
        for item in self.items:
            item.process_draw()
