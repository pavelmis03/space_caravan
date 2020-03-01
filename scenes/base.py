import pygame

from constants import Color
from geometry.point import Point


class Scene:
    def __init__(self, game):
        self.game = game
        self.screen = self.game.screen
        self.interface_objects = []
        self.game_objects = []
        self.create_objects()

    def create_objects(self):
        pass

    def iteration(self):
        self.process_all_logic()
        self.process_all_draw()

    def process_all_logic(self):
        for item in self.interface_objects:
            item.process_logic()
        for item in self.game_objects:
            item.process_logic()
        self.additional_logic()

    def process_all_draw(self):
        self.screen.fill(Color.BLACK)
        for item in self.interface_objects:
            item.process_draw()
        for item in self.game_objects:
            item.process_draw(Point(0, 0))
        self.additional_draw()
        pygame.display.flip()  # double buffering
        pygame.time.wait(10)  # подождать 10 миллисекунд
    
    def additional_logic(self):
        pass
    
    def additional_draw(self):
        pass
