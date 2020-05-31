import pygame

from pygame import Rect
from typing import Dict

from scenes.game.base import GameScene
from space.planets_generator import PlanetsGenerator
from constants.color import COLOR
from utils.game_data_manager import from_list_of_dicts, to_list_of_dicts


class SpacemapScene(GameScene):
    """
    Сцена звездной карты.

    :param game: игра, создающая сцену
    """
    DATA_FILENAME = 'spacemap'
    PANEL_HEIGHT = 100

    def __init__(self, game):
        super().__init__(game, self.DATA_FILENAME)
        self.planets = list()

    def initialize(self):
        """
        Для звездной карты инициализация означает создание планет, чем занимается PlanetsGenerator.
        """
        planets_generator = PlanetsGenerator(self.game.controller, self)
        self.planets = planets_generator.generate()

    def from_dict(self, data_dict: Dict):
        super().from_dict(data_dict)
        self.planets = from_list_of_dicts(self, data_dict['planets'])

    def to_dict(self) -> Dict:
        result = super().to_dict()
        result.update({
            'planets': to_list_of_dicts(self.planets),
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

    def planets_logic(self):
        for planet in self.planets:
            planet.process_logic()

    def process_all_logic(self):
        super().process_all_logic()
        self.planets_logic()
