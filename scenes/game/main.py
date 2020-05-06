from typing import Dict

from drawable_objects.ladder import Ladder
from drawable_objects.interface.ammo_display import AmmoDisplay
from drawable_objects.interface.pause_manager import PauseManager
from drawable_objects.interface.player_icon import PlayerIcon
from scenes.game.base import GameScene
from geometry.point import Point
from map.level.grid import LevelGrid


class MainScene(GameScene):
    """
    Класс главной игровой сцены. Называется так, потому что пока это единственная игровая сцена.

    :param game: игра, создающая сцену
    """

    def __init__(self, game):
        super().__init__(game)
        player_icon = PlayerIcon(self, self.game.controller, self.player)
        self.interface_objects.append(player_icon)
        ammo_display = AmmoDisplay(self, self.game.controller, Point(100, 20), self.player.weapon)
        self.interface_objects.append(ammo_display)

    def initialize(self):
        super().initialize()
        self.grid = LevelGrid(self, self.game.controller, Point(0, 0), 25, 25)
        self.game_objects.append(Ladder(
            self, self.game.controller, Point(85, 150), 0))

    def from_dict(self):
        super().from_dict()

    def to_dict(self) -> Dict:
        result = super().to_dict()
        return result

    def process_all_logic(self):
        super().process_all_logic()
        pass

    def process_all_draw(self):
        super().process_all_draw()
        return
        pass
