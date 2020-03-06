from constants import Color
from drawable_objects.player import Player
from scenes.base import GameScene
from geometry.point import Point

from map.grid import GeneratedGird


class MainScene(GameScene):
    def __init__(self, game):
        super().__init__(game)
        self.player = Player(self, self.game.controller, Point(0, 0), 0)
        self.grid = GeneratedGird(self, self.game.controller, 1, 1)

    def process_all_logic(self):
        super().process_all_logic()
        pass

    def process_all_draw(self):
        super().process_all_draw()
        pass
