import sys

import pygame

from controller.controller import Controller
from space.space import Space
from geometry.rectangle import Rectangle
from scenes.main import MainScene
from scenes.spaceship_scene import SpaceshipScene
from scenes.menu.about import AboutMenuScene
from scenes.menu.main import MainMenuScene
from scenes.menu.settings import SettingsMenuScene
from utils.image import ImageManager
from typing import Tuple


class Game:
    MAIN_MENU_SCENE_INDEX = 0
    MAIN_SCENE_INDEX = 1
    SETTINGS_MENU_SCENE_INDEX = 2
    ABOUT_MENU_SCENE_INDEX = 3
    SPACESHIP_SCENE_INDEX = 4
    SPACEMAP_SCENE_INDEX = 5
    GAMEOVER_SCENE_INDEX = 6

    def __init__(self, width: int = 1000, height: int = 700):
        pygame.init()
        self.size = (width, height)
        self.__running = True
        ImageManager.load_all()

        self.__controller = Controller(self)
        self.__space = Space(self, self.__controller)
        self.__scenes = [
            MainMenuScene(self),
            MainScene(self),
            SettingsMenuScene(self),
            AboutMenuScene(self),
            SpaceshipScene(self),
            self.__space.get_spacemap_scene(),
        ]
        self.__current_scene = 0

    @property
    def size(self) -> Tuple[int, int]:
        return self.__size

    @size.setter
    def size(self, value: Tuple[int, int]):
        """
        Присвоением окну размера инициализируются все характеристики экрана.
        """
        self.__size = value
        self.__width = self.__size[0]
        self.__height = self.__size[1]
        self.__screen_rectangle = Rectangle(0, 0, self.__width, self.__height)
        self.__create_window()

    def __create_window(self):
        self.__screen = pygame.display.set_mode(self.__size, pygame.RESIZABLE)

    @property
    def screen(self) -> pygame.Surface:
        return self.__screen

    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height

    @property
    def screen_rectangle(self) -> Rectangle:
        return self.__screen_rectangle

    @property
    def controller(self) -> Controller:
        return self.__controller

    def set_scene(self, scene_index):
        self.__current_scene = scene_index

    def end(self):
        self.__running = False

    def main_loop(self):
        while self.__running:
            self.__controller.iteration()
            self.__scenes[self.__current_scene].iteration()
        sys.exit(0)
