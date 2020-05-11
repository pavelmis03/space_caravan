from typing import Dict

from scenes.spacemap import SpacemapScene
from scenes.game.spaceship import SpaceshipScene
from space.planets_generator import PlanetsGenerator
from geometry.rectangle import Rectangle
from drawable_objects.player import Player


class Space:
    PLANETS_NUMBER = 12

    def __init__(self, game, name='world'):
        self.__game = game
        self.__controller = game.controller
        self.__name = name
        self.__spacemap_scene = SpacemapScene(self.__game)
        self.__spaceship_scene = SpaceshipScene(self.__game)
        self.__planets = None

    def initialize(self):
        space_rectangle = Rectangle(0, 0, self.__game.width, self.__game.height)
        planets_generator = PlanetsGenerator(space_rectangle, Space.PLANETS_NUMBER, self.__controller,
                                             self.__spacemap_scene)
        self.__planets = planets_generator.generate()
        self.__spacemap_scene.interface_objects = self.__planets

        self.__game.file_manager.reset()
        self.__game.file_manager.create_space_storage(self.__name)

    def load(self):
        pass

    def save(self):
        pass

    @property
    def spacemap_scene(self):
        return self.__spacemap_scene

    @property
    def spaceship_scene(self):
        return self.__spaceship_scene
