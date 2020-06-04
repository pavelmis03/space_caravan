from typing import Dict

from drawable_objects.interface.essence_display import EssenceDisplay
from drawable_objects.ladder import Ladder
from drawable_objects.interface.ammo_display import AmmoDisplay
from drawable_objects.interface.player_icon import PlayerIcon
from drawable_objects.interface.weapons_display import WeaponsDisplay
from drawable_objects.interface.enemy_count_display import EnemyCountDisplay
from scenes.game.level import LevelScene
from geometry.point import Point
from map.level.grid import LevelGrid, DemoLevel


class MainScene(LevelScene):
    """
    Класс главной игровой сцены - сцены уровня.

    :param game: игра, создающая сцену
    :param planet_index: индекс планеты, создавшей уровень
    """

    def __init__(self, game, planet_index: str):
        super().__init__(game, 'planet' + str(planet_index))
        self.planet_index = planet_index
        enemy_count_display = EnemyCountDisplay(self, self.game.controller,
                                                (1, 0.1), self.enemies)
        self.interface_objects.append(enemy_count_display)

    def initialize(self):
        super().initialize()

        biom = self.common_data.planet_biom[self.planet_index]
        if biom == 0: # demo biom:
            self.grid = DemoLevel(self, self.game.controller, Point(0, 0))
        else:
            self.grid = LevelGrid(self, self.game.controller, Point(0, 0))
        self.grid.biom = biom
        self.grid.initialize()

        self.game_objects.append(Ladder(
            self, self.game.controller, Point(85, 150), 0))

    def from_dict(self, data_dict: Dict):
        super().from_dict(data_dict)
        self.grid = LevelGrid(self, self.game.controller, Point(0, 0))
        self.grid.from_dict(data_dict['grid'])

    def to_dict(self) -> Dict:
        result = super().to_dict()
        result.update({'grid': self.grid.to_dict()})
        return result

    def save(self):
        """
        Во избежание ошибок враги подсчитываются перед самым сохранением сцены.
        """
        if len(self.enemies) == 0:
            self.common_data.planet_completed[self.planet_index] = True
        super().save()
