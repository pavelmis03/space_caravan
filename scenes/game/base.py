from typing import Dict, List

from scenes.conservable import ConservableScene
from utils.game_data_manager import from_list_of_dicts, to_list_of_dicts
from space.supply import Supply


class GameScene(ConservableScene):
    """

    :param game: игра, создающая сцену
    :param data_filename: имя файла, в который сохраняется сцена (расширение не указывать)
    """

    def __init__(self, game, data_filename: str):
        super().__init__(game, data_filename)
        self.data_filename = data_filename
        self.supply = None

    def load_supply(self):
        self.supply = Supply(self)
        self.supply.load()

    def save(self):
        super().save()
        self.supply.save()

    def from_dict(self, data_dict: Dict):
        super().from_dict(data_dict)
        self.interface_objects += from_list_of_dicts(
            self, data_dict['interface_objects'])

    def to_dict(self) -> Dict:
        result = super().to_dict()
        result.update({
            'interface_objects': to_list_of_dicts(self.interface_objects)
        })
        return result
