from drawable_objects.console import Console
from console.entry import Entry
from drawable_objects.player import Player
from scenes.base import GameScene
from geometry.point import Point
from map.level.grid import LevelGrid
from utils.game_plane import GamePlane


class MainScene(GameScene):
    """
    Класс главной игровой сцены. Называется так, потому что пока это единственная игровая сцена.

    :param game: игра, создающая сцену
    """
    def __init__(self, game):
        super().__init__(game)
        self.plane = GamePlane()
        self.player = Player(self, self.game.controller, Point(0, 0), 0)
        self.game.controller.input_objects.append(self.player)
        self.grid = LevelGrid(self, self.game.controller, Point(0, 0), 25, 25)

        cmd = Console(self, self.game.controller, Point(600, 600))
        self.interface_objects.append(cmd)
        # self.consoleEntry = Entry(self, self.game.controller, (0, self.game.height-20, 200, self.game.height), "kek")
        # self.interface_objects.append(self.consoleEntry)

    def process_all_logic(self):
        super().process_all_logic()
        pass

    def process_all_draw(self):
        super().process_all_draw()
        pass
