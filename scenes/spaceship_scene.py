from console.console import Console
from console.entry import Entry
from drawable_objects.interface.pause_manager import PauseManager
from drawable_objects.player import Player
from scenes.base import GameScene
from geometry.point import Point
from map.level.grid import SpaceshipGrid
from utils.game_plane import GamePlane


class SpaceshipScene(GameScene):
    def __init__(self, game):
        super ().__init__ (game)
        self.plane = GamePlane ()
        self.player = Player (self, self.game.controller, Point (100, 100), 0)
        self.game.controller.input_objects.append (self.player)
        self.grid = SpaceshipGrid(self, self.game.controller, Point (0, 0), 25, 25)

        self.pause_manager = PauseManager (self, self.game.controller)
        self.interface_objects.append (self.pause_manager)
        self.game.controller.input_objects.append (self.pause_manager)

