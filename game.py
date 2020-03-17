import sys

import pygame

from controller.controller import Controller
from geometry.rectangle import Rectangle
from scenes.main import MainScene
from scenes.menu_about import About_MenuScene
from scenes.menu_main import Main_MenuScene
from scenes.menu_settings import Settings_MenuScene
from utils.image import ImageManager
from typing import Tuple

class Game:
    MAIN_MENU_SCENE_INDEX = 0
    MAIN_SCENE_INDEX = 1
    SETTINGS_MENU_SCENE_INDEX = 2
    ABOUT_MENU_SCENE_INDEX = 3
    GAMEOVER_SCENE_INDEX = 4

    def __init__(self, width=800, height=600):
        self.size = (width, height)

        self.screen = None
        pygame.init()
        self.create_window()
        self.running = True
        self.controller = Controller(self)
        self.scenes = [Main_MenuScene(self), MainScene(self), Settings_MenuScene(self), About_MenuScene(self)]
        self.current_scene = 0

        ImageManager.load_all()

    @property
    def size(self) -> Tuple[int, int]:
        return self._size

    @size.setter
    def size(self, value: Tuple[int, int]):
        self._size = value
        self.width = self._size[0]
        self.height = self._size[1]
        self.screen_rectangle = Rectangle(0, 0, self.width, self.height)
        self.create_window()

    def create_window(self):
        self.screen = pygame.display.set_mode(self.size, pygame.RESIZABLE)

    def set_scene(self, scene_index):
        self.current_scene = scene_index

    def end(self):
        self.running = False

    def main_loop(self):
        while self.running:
            self.controller.iteration()
            self.scenes[self.current_scene].iteration()
        sys.exit(0)