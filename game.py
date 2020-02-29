import sys
import pygame

from scenes.final import FinalScene
from scenes.main import MainScene
from scenes.menu import MenuScene


class Game:
    MENU_SCENE_INDEX = 0
    MAIN_SCENE_INDEX = 1
    GAMEOVER_SCENE_INDEX = 2

    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.size = self.width, self.height

        self.create_window()
        self.running = True
        self.scenes = [MenuScene(self), MainScene(self), FinalScene(self)]
        self.current_scene = 0

    def create_window(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.size, pygame.RESIZABLE)

    def main_loop(self):
        while self.running:
            eventlist = pygame.event.get()
            for event in eventlist:
                if event.type == pygame.QUIT:
                    print('Пользователь нажал крестик')
                    self.running = False
            self.scenes[self.current_scene].process_frame(self.screen, eventlist)
        sys.exit(0)