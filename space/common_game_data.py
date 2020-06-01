from typing import Dict

from scenes.base import Scene


class CommonGameData:
    """
    Объект с общими данными игры, которые нужны всем игровым сценам. Здесь хранятся запасы ресурсов игрока,
    некоторые данные о планетах.
    """
    START_FUEL = 1000
    START_ESSENCE = 0

    DATA_FILENAME = 'common_game_data'

    def __init__(self, scene: Scene):
        self.__scene = scene
        self.fuel = 0
        self.essence = 0
        self.planet_biom = {}
        self.planet_completed = {}

    def initialize(self):
        self.fuel = self.START_FUEL
        self.essence = self.START_ESSENCE

    def from_dict(self, data_dict: Dict):
        self.fuel = data_dict['fuel']
        self.essence = data_dict['essence']
        self.planet_biom = data_dict['planet_biom']
        self.planet_completed = data_dict['planet_completed']

    def to_dict(self) -> Dict:
        return {
            'fuel': self.fuel,
            'essence': self.essence,
            'planet_biom': self.planet_biom,
            'planet_completed': self.planet_completed,
        }

    def load(self):
        self.from_dict(self.__scene.game.file_manager.read_data(self.DATA_FILENAME))

    def save(self):
        self.__scene.game.file_manager.write_data(self.DATA_FILENAME, self.to_dict())
