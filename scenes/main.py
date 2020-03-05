from constants import Color
from drawable_objects.player import Player
from scenes.base import Scene
from geometry.point import Point

from map.grid import GeneratedGird

class MainScene(Scene):

    def create_objects(self):
        self.player = Player(self, self.game.controller, Point(self.game.width / 2, self.game.height / 2), 0)
        self.game_objects = [self.player]
        self.grid = GeneratedGird(self, self.game.controller, 1, 1)

    def additional_draw(self):
        self.grid.process_draw(self.player.pos)
