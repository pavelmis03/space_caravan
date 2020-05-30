from typing import Dict

from drawable_objects.ladder import Ladder
from drawable_objects.interface.ammo_display import AmmoDisplay
from drawable_objects.interface.player_icon import PlayerIcon
from drawable_objects.interface.weapons_display import WeaponsDisplay
from drawable_objects.interface.enemy_count_display import EnemyCountDisplay
from scenes.game.base import GameScene
from geometry.point import Point
from map.level.grid import LevelGrid


class MainScene(GameScene):
    """
    Класс главной игровой сцены - сцены уровня.

    :param game: игра, создающая сцену
    :param data_filename: имя файла, в который сохраняется сцена (расширение не указывать)
    """

    def __init__(self, game, data_filename: str):
        super().__init__(game, data_filename)

    def initialize(self):
        super().initialize()

        self.grid = LevelGrid(self, self.game.controller, Point(0, 0))
        self.grid.biom = self.__biom
        self.grid.initialize()

        self.game_objects.append(Ladder(
            self, self.game.controller, Point(85, 150), 0))

    def set_biom(self, biom: int):
        self.__biom = biom

    def from_dict(self, data_dict: Dict):
        super().from_dict(data_dict)
        self.grid = LevelGrid(self, self.game.controller, Point(0, 0))
        self.grid.from_dict(data_dict['grid'])

    def to_dict(self) -> Dict:
        result = super().to_dict()
        result.update({'grid': self.grid.to_dict()})
        return result

    def load_player(self):
        super().load_player()
        player_icon = PlayerIcon(self, self.game.controller, self.player)
        self.interface_objects.append(player_icon)

        weapons_display = WeaponsDisplay(self.player, Point(100, 0))
        self.interface_objects.append(weapons_display)
        ammo_display = AmmoDisplay(self, self.game.controller, Point(240, 20), self.player.weapon)
        self.interface_objects.append(ammo_display)

        enemy_count_display = EnemyCountDisplay(self, self.game.controller,
                                                (1, 0), self.enemies)
        self.interface_objects.append(enemy_count_display)
