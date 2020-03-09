import sys
import pygame

from scenes.final import FinalScene
from scenes.main import MainScene
from scenes.menu import MenuScene
from controller.controller import Controller

from geometry.point import Point

from utils.image import ImageManager

class Game:
    MENU_SCENE_INDEX = 0
    MAIN_SCENE_INDEX = 1
    GAMEOVER_SCENE_INDEX = 2

    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.center = Point(self.width / 2, self.height / 2)
        self.size = self.width, self.height

        self.screen = None
        self.create_window()
        self.running = True
        self.controller = Controller(self)
        self.scenes = [MenuScene(self), MainScene(self)]
        self.current_scene = 0

        ImageManager.load_all()

    def create_window(self):
        pygame.init()
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