import sys
import pygame

from typing import Tuple

from controller.controller import Controller
from geometry.rectangle import Rectangle
from scenes.base import Scene, ConservableScene
from scenes.game.spaceship import SpaceshipScene
from scenes.game.base import GameScene
from scenes.menu.about import AboutMenuScene
from scenes.menu.main import MainMenuScene
from scenes.menu.settings import SettingsMenuScene
from utils.image import ImageManager
from utils.file_manager import FileManager
from utils.sound import SoundManager


class Game:
    MAIN_MENU_SCENE_INDEX = 0
    SETTINGS_MENU_SCENE_INDEX = 1
    ABOUT_MENU_SCENE_INDEX = 2

    def __init__(self, width: int = 1000, height: int = 700):
        pygame.init()
        self.size = (width, height)
        self.__running = True
        ImageManager.load_all()
        SoundManager.load_all()
        self.__file_manager = FileManager()

        self.__controller = Controller(self)
        self.__scenes = [
            MainMenuScene(self),
            SettingsMenuScene(self),
            AboutMenuScene(self),
        ]
        self.__current_scene = self.__scenes[0]

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

    @property
    def file_manager(self) -> FileManager:
        return self.__file_manager

    def set_scene(self, scene: Scene, player_loading_needed: bool = True):
        if isinstance(self.__current_scene, ConservableScene):
            self.__current_scene.save()
        if player_loading_needed and isinstance(scene, GameScene):
            scene.load_player()
        self.__current_scene = scene

    def set_scene_with_index(self, scene_index: int):
        self.set_scene(self.__scenes[scene_index])

    def start_new_game(self):
        self.file_manager.reset()
        self.file_manager.create_space_storage('world')
        spaceship_scene = SpaceshipScene(self)
        spaceship_scene.initialize()
        self.set_scene(spaceship_scene, False)

    def end(self):
        self.__running = False

    def main_loop(self):
        while self.__running:
            self.__controller.iteration()
            self.__current_scene.iteration()
        sys.exit(0)
