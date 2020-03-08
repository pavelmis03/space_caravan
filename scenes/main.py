from constants import Color
from drawable_objects.console import Console
from drawable_objects.player import Player
from scenes.base import Scene
from geometry.point import Point

class MainScene(Scene):

    def create_objects(self):
        self.player = Player(self, self.game.controller, Point(400, 400), 0)
        self.game.controller.input_objects.append(self.player)
        self.game_objects = [self.player]
        cmd = Console(self, self.game.controller, Point(600, 600))
        self.game_objects.append(cmd)
