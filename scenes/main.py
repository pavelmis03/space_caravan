from console.console import Console
from console.entry import Entry
from drawable_objects.Ladder import Ladder
from drawable_objects.interface.ammo_display import AmmoDisplay
from drawable_objects.interface.display_count import DisplayCount
from drawable_objects.interface.pause_manager import PauseManager
from drawable_objects.interface.player_icon import PlayerIcon
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
        self.player = Player(self, self.game.controller, Point(100, 100), 0)
        self.game.controller.input_objects.append(self.player)
        self.grid = LevelGrid(self, self.game.controller, Point(0, 0), 25, 25)

        self.game_objects.append(Ladder(
            self, self.game.controller, Point(85, 150), 0))

        self.pause_manager = PauseManager(self, self.game.controller)
        self.interface_objects.append(self.pause_manager)
        self.game.controller.input_objects.append(self.pause_manager)

        player_icon = PlayerIcon(self, self.game.controller, self.player)
        self.interface_objects.append(player_icon)

        ammo_display = AmmoDisplay(self, self.game.controller, Point(100, 20), self.player.weapon)
        self.interface_objects.append(ammo_display)
        # cmd = Console(self, self.game.controller, (0, self.game.height-20, 200, self.game.height))
        # self.interface_objects.append(cmd)

    def process_all_logic(self):
        super().process_all_logic()
        pass

    def process_all_draw(self):
        super().process_all_draw()
        return
        pass
