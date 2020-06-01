import pygame

from pygame import Rect
from typing import Dict

from scenes.game.base import GameScene
from space.planets_generator import PlanetsGenerator
from space.travel_cost_counter import TravelCostCounter
from constants.color import COLOR
from utils.game_data_manager import from_list_of_dicts, to_list_of_dicts
from drawable_objects.menu.button import Button
from drawable_objects.menu.label import Label
from drawable_objects.spaceship_icon import SpaceshipIcon
from geometry.point import Point


class PanelArranger:
    """
    Расстановщик виджетов меню на панели космической карты.

    :param scene: сцена космической карты, создающая объект
    """
    def __init__(self, scene):
        self.__scene = scene
        self.__widgets = []

    def add_widget(self, widget, relative_pos: Point):
        """
        Добавление виджета с его позицией относительно левого верхнего угла панели.
        """
        self.__widgets.append((widget, relative_pos))
        self.__scene.interface_objects.append(widget)

    def process_logic(self):
        """
        Логика объекта - перемещение виджетов на свои места на панели.
        """
        relative_center = Point(0, self.__scene.game.height - self.__scene.PANEL_HEIGHT)
        for item in self.__widgets:
            target_top_left = relative_center + item[1]
            movement_vector = target_top_left - item[0].geometry.top_left
            item[0].move(movement_vector)


class SpacemapScene(GameScene):
    """
    Сцена космической карты. Содержит список планет и виджеты панели управления кораблем. Корабль игрока всегда
    около одной из планет - текущей. Можно выбирать планеты и перелетать к ним.

    :param game: игра, создающая сцену
    """
    DATA_FILENAME = 'spacemap'

    PANEL_BG_COLOR = COLOR['BLUE']
    CHOICE_ALLOWED_COLOR = COLOR['GREEN']
    CHOICE_UNALLOWED_COLOR = COLOR['RED']

    REVOLVING_RADIUS = 50
    CHOICE_VIEW_RADIUS = 35

    WIDGET_WIDTH = 200
    WIDGET_HEIGHT = 60
    WIDGET_INDENT_LEFT = 20
    WIDGET_INDENT_TOP = 10
    PANEL_HEIGHT = WIDGET_HEIGHT + 2 * WIDGET_INDENT_TOP
    BUTTON_GEOMETRY = (0, 0, WIDGET_WIDTH, WIDGET_HEIGHT)
    LABEL_HEIGHT = (WIDGET_HEIGHT - WIDGET_INDENT_TOP) // 2
    LABEL_GEOMETRY = (0, 0, WIDGET_WIDTH, LABEL_HEIGHT)

    def __init__(self, game):
        super().__init__(game, self.DATA_FILENAME)
        self.planets = list()
        self.choice = None
        self.current_planet = None
        self.travel_cost_counter = TravelCostCounter()
        self.spaceship_icon = SpaceshipIcon(self, self.game.controller, self.REVOLVING_RADIUS)
        self.interface_objects.append(self.spaceship_icon)
        self.panel_arranger = PanelArranger(self)

        land_button = Button(self, self.game.controller, self.BUTTON_GEOMETRY, 'Высадиться', self.run_level)
        travel_button = Button(self, self.game.controller, self.BUTTON_GEOMETRY, 'Перелететь', self.travel)
        self.fuel_label = Label(self, self.LABEL_GEOMETRY, '', 'left')
        self.cost_label = Label(self, self.LABEL_GEOMETRY, '', 'left')
        back_button = Button(self, self.game.controller, self.BUTTON_GEOMETRY, 'Назад', self.back_to_spaceship)
        self.panel_arranger.add_widget(land_button, Point(2 * self.WIDGET_INDENT_LEFT, self.WIDGET_INDENT_TOP))
        self.panel_arranger.add_widget(travel_button, Point(3 * self.WIDGET_INDENT_LEFT + self.WIDGET_WIDTH,
                                                            self.WIDGET_INDENT_TOP))
        self.panel_arranger.add_widget(self.fuel_label, Point(4 * self.WIDGET_INDENT_LEFT + 2 * self.WIDGET_WIDTH,
                                                              self.WIDGET_INDENT_TOP))
        self.panel_arranger.add_widget(self.cost_label, Point(4 * self.WIDGET_INDENT_LEFT + 2 * self.WIDGET_WIDTH,
                                                              2 * self.WIDGET_INDENT_TOP + self.LABEL_HEIGHT))
        self.panel_arranger.add_widget(back_button, Point(5 * self.WIDGET_INDENT_LEFT + 3 * self.WIDGET_WIDTH,
                                                          self.WIDGET_INDENT_TOP))

    def initialize(self):
        """
        Для звездной карты инициализация означает создание планет, чем занимается PlanetsGenerator.
        """
        planets_generator = PlanetsGenerator(self.game.controller, self)
        self.planets = planets_generator.generate()
        self.current_planet = self.planets[0]
        for planet in self.planets:
            planet.add_to_common_data()

    def from_dict(self, data_dict: Dict):
        super().from_dict(data_dict)
        self.planets = from_list_of_dicts(self, data_dict['planets'])
        for planet in self.planets:
            if planet.index == data_dict['current_planet_index']:
                self.current_planet = planet

    def to_dict(self) -> Dict:
        result = super().to_dict()
        result.update({
            'planets': to_list_of_dicts(self.planets),
            'current_planet_index': self.current_planet.index
        })
        return result

    def draw_terminal_window(self):
        """
        Отрисовка элементов окна терминала: рамки вокруг космической карты и прямоугольника панели управления
        кораблем.
        """
        window_rect = Rect(0, 0, self.game.width, self.game.height)
        panel_rect = Rect(0, self.game.height - self.PANEL_HEIGHT, self.game.width, self.PANEL_HEIGHT)
        pygame.draw.rect(self.screen, self.PANEL_BG_COLOR, window_rect, 2)
        pygame.draw.rect(self.screen, self.PANEL_BG_COLOR, panel_rect)

    def interface_draw(self):
        self.draw_terminal_window()
        super().interface_draw()

    def mark_choice(self):
        """
        Отметка выбранной планеты (одного из двух типов в зависимости от того, возможно ли долететь до нее).
        """
        if self.choice:
            if self.is_travel_possible():
                choice_color = self.CHOICE_ALLOWED_COLOR
            else:
                choice_color = self.CHOICE_UNALLOWED_COLOR
            integer_pos = (round(self.choice.pos.x), round(self.choice.pos.y))
            pygame.draw.circle(self.screen, choice_color, integer_pos, self.CHOICE_VIEW_RADIUS)

    def planets_draw(self):
        self.mark_choice()
        for planet in self.planets:
            planet.process_draw()

    def process_all_draw(self):
        super().process_all_draw()
        self.planets_draw()

    def labels_update(self):
        """
        Обновление текста надписей на панели управления кораблем.
        """
        self.fuel_label.update_text('Топливо: {}'.format(self.common_data.fuel))
        cost = '---'
        if self.choice:
            cost = self.get_current_cost()
        self.cost_label.update_text('Стоимость: {}'.format(cost))

    def interface_logic(self):
        self.panel_arranger.process_logic()
        super().interface_logic()
        self.labels_update()

    def planets_logic(self):
        """
        Логика планет: собственно вызов логики у планет, поиск выбранной пользователем планеты и логика иконки
        космического корабля. Текущую планету выбрать нельзя.
        """
        for planet in self.planets:
            planet.process_logic()
        self.choice = None
        for planet in self.planets:
            if planet.chosen and planet != self.current_planet:
                self.choice = planet
        self.spaceship_icon.set_planet_pos(self.current_planet.pos)

    def process_all_logic(self):
        super().process_all_logic()
        self.planets_logic()

    def get_current_cost(self):
        """
        Стоимость перелета на выбранную планету.
        """
        return self.travel_cost_counter.get_cost(self.current_planet, self.choice)

    def is_travel_possible(self):
        return self.get_current_cost() <= self.common_data.fuel

    def run_level(self):
        self.current_planet.run_level()

    def travel(self):
        """
        Перелет от текущей планеты к выбранной пользователем, если это возможно.
        """
        if self.choice:
            if not self.is_travel_possible():
                return
            self.common_data.fuel -= self.get_current_cost()
            self.current_planet = self.choice

    def back_to_spaceship(self):
        """
        Возвращение на корабль - установка соответствующей сцены.
        """
        from scenes.game.spaceship import SpaceshipScene
        spaceship_scene = SpaceshipScene(self.game)
        self.game.set_scene(spaceship_scene)
