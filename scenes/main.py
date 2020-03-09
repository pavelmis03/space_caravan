from constants import Color
from drawable_objects.player import Player
from scenes.base import GameScene
from geometry.point import Point

from map.level.grid import LevelGrid


class MainScene(GameScene):
    def __init__(self, game):
        super().__init__(game)
        self.player = Player(self, self.game.controller, Point(0, 0), 0)
        self.grid = LevelGrid(self, self.game.controller, Point(0, 0), 25, 25)

    def process_all_logic(self):
        super().process_all_logic()
        pass

    def process_all_draw(self):
        super().process_all_draw()
        pass
