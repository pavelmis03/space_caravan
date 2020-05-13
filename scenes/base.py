import pygame

from typing import Dict, List

from constants.color import COLOR
from constants.saving import CLASSES_BASE
from geometry.point import Point


class Scene:
    """
    Базовый класс сцены.

    :param game: игра, создающая сцену
    """

    CLEAR_COLOR = COLOR['BLACK']

    def __init__(self, game):
        self.game = game
        self.screen = self.game.screen
        self.interface_objects = []

    @property
    def width(self):
        return self.game.width

    @property
    def height(self):
        return self.game.height

    @property
    def center(self):
        return Point(self.width / 2, self.height / 2)

    def iteration(self):
        """
        Итерация работы сцены - обработка логики и отрисовка. Далее команда двойной буферизации и задержка
        между тактами.
        """
        self.process_all_logic()
        self.process_all_draw()
        pygame.display.flip()
        pygame.time.wait(10)

    def interface_logic(self):
        for item in self.interface_objects:
            item.process_logic()

    def process_all_logic(self):
        """
        Логика сцены и ее объектов.
        """
        self.interface_logic()

    def clear_screen(self):
        self.screen.fill(self.CLEAR_COLOR)

    def interface_draw(self):
        for item in self.interface_objects:
            item.process_draw()

    def process_all_draw(self):
        """
        Отрисовка сцены и ее объектов.
        """
        self.clear_screen()
        self.interface_draw()


class ConservableScene(Scene):
    def __init__(self, game, data_filename: str):
        super().__init__(game)
        self.data_filename = data_filename

    def initialize(self):
        pass

    def from_dict(self, data_dict: Dict):
        self.interface_objects = self.from_list_of_dicts(data_dict['interface_objects'])

    def to_dict(self) -> Dict:
        return {
            'interface_objects': self.to_list_of_dicts(self.interface_objects)
        }

    def to_list_of_dicts(self, objects: List) -> List[Dict]:
        result = list()
        for item in objects:
            if item in CLASSES_BASE.values():
                result.append(item.to_dict())
        return result

    def from_list_of_dicts(self, data_list: List[Dict]) -> List:
        result = list()
        for item in data_list:
            new_object = CLASSES_BASE[item['classname']](self, self.game.controller)
            new_object.from_dict(item)
            self.interface_objects.append(new_object)
        return result

    def load(self):
        self.from_dict(self.game.file_manager.read_data(self.data_filename))

    def save(self):
        self.game.file_manager.write_data(self.data_filename, self.to_dict())
