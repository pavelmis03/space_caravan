from typing import Dict

from scenes.base import Scene


class Supply:
    """
    Припасы - хранилище ресурсов, запасного оружия и прочего. Существует на всех сохраняемых сценах (игровых и
    звездной карте).
    """
    START_FUEL = 0
    START_ESSENCE = 0

    DATA_FILENAME = 'supply'

    def __init__(self, scene: Scene):
        self.__scene = scene
        self.fuel = 0
        self.essence = 0

    def initialize(self):
        self.fuel = self.START_FUEL
        self.essence = self.START_ESSENCE

    def from_dict(self, data_dict: Dict):
        self.fuel = data_dict['fuel']
        self.essence = data_dict['essence']

    def to_dict(self) -> Dict:
        return {
            'fuel': self.fuel,
            'essence': self.essence,
        }

    def load(self):
        self.from_dict(self.__scene.game.file_manager.read_data(self.DATA_FILENAME))

    def save(self):
        self.__scene.game.file_manager.write_data(self.DATA_FILENAME, self.to_dict())
