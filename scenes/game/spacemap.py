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
    def __init__(self, scene):
        self.__scene = scene
        self.__widgets = []

    def add_widget(self, widget, relative_pos: Point):
        self.__widgets.append((widget, relative_pos))

    def process_logic(self):
        relative_center = Point(0, self.__scene.game.height - self.__scene.PANEL_HEIGHT)
        for item in self.__widgets:
            target_top_left = relative_center + item[1]
            movement_vector = target_top_left - item[0].geometry.top_left
            item[0].move(movement_vector)


class SpacemapScene(GameScene):
    """
    Сцена звездной карты.

    :param game: игра, создающая сцену
    """
    DATA_FILENAME = 'spacemap'
    PANEL_HEIGHT = 80
    REVOLVING_RADIUS = 50

    def __init__(self, game):
        super().__init__(game, self.DATA_FILENAME)
        self.planets = list()
        self.choice = None
        self.current_planet = None
        self.travel_cost_counter = TravelCostCounter()
        self.spaceship_icon = SpaceshipIcon(self, self.game.controller, self.REVOLVING_RADIUS)
        self.interface_objects.append(self.spaceship_icon)
        self.panel_arranger = PanelArranger(self)

        land_button = Button(self, self.game.controller, (0, 0, 150, 60), 'Высадиться', self.run_level)
        travel_button = Button(self, self.game.controller, (0, 0, 150, 60), 'Перелететь', self.travel)
        self.fuel_label = Label(self, (0, 0, 150, 20), '---', 'left')
        self.cost_label = Label(self, (0, 0, 150, 20), '---', 'left')
        self.interface_objects.append(land_button)
        self.interface_objects.append(travel_button)
        self.interface_objects.append(self.fuel_label)
        self.interface_objects.append(self.cost_label)
        self.panel_arranger.add_widget(land_button, Point(20, 10))
        self.panel_arranger.add_widget(travel_button, Point(190, 10))
        self.panel_arranger.add_widget(self.fuel_label, Point(360, 10))
        self.panel_arranger.add_widget(self.cost_label, Point(360, 40))

    def initialize(self):
        """
        Для звездной карты инициализация означает создание планет, чем занимается PlanetsGenerator.
        """
        planets_generator = PlanetsGenerator(self.game.controller, self)
        self.planets = planets_generator.generate()
        self.current_planet = self.planets[0]

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
        window_rect = Rect(0, 0, self.game.width, self.game.height)
        panel_rect = Rect(0, self.game.height - self.PANEL_HEIGHT, self.game.width, self.PANEL_HEIGHT)
        pygame.draw.rect(self.screen, COLOR['BLUE'], window_rect, 2)
        pygame.draw.rect(self.screen, COLOR['BLUE'], panel_rect)

    def interface_draw(self):
        self.draw_terminal_window()
        super().interface_draw()

    def planets_draw(self):
        for planet in self.planets:
            planet.process_draw()

    def process_all_draw(self):
        super().process_all_draw()
        self.planets_draw()

    def interface_logic(self):
        self.panel_arranger.process_logic()
        self.fuel_label.update_text('Топливо: ' + str(self.common_data.fuel))
        if self.choice and self.choice != self.current_planet:
            cost = self.travel_cost_counter.get_cost(self.current_planet, self.choice)
            self.cost_label.update_text('Стоимость: ' + str(cost))
        else:
            self.cost_label.update_text('Стоимость: ---')
        super().interface_logic()

    def planets_logic(self):
        for planet in self.planets:
            planet.process_logic()
        self.choice = None
        for planet in self.planets:
            if planet.chosen:
                self.choice = planet
        self.spaceship_icon.set_planet_pos(self.current_planet.pos)

    def process_all_logic(self):
        super().process_all_logic()
        self.planets_logic()

    def run_level(self):
        self.current_planet.run_level()

    def travel(self):
        if self.choice and self.current_planet != self.choice:
            cost = self.travel_cost_counter.get_cost(self.current_planet, self.choice)
            if cost > self.common_data.fuel:
                return
            self.common_data.fuel -= cost
            self.current_planet = self.choice
