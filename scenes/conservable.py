from typing import Dict, List

from constants.saving import CLASSES_BASE
from scenes.base import Scene


class ConservableScene(Scene):
    def __init__(self, game, data_filename: str):
        super().__init__(game)
        self.data_filename = data_filename

    def initialize(self):
        pass

    def from_dict(self, data_dict: Dict):
        self.interface_objects += self.from_list_of_dicts(data_dict['interface_objects'])

    def to_dict(self) -> Dict:
        return {
            'interface_objects': self.to_list_of_dicts(self.interface_objects)
        }

    def to_list_of_dicts(self, objects: List) -> List[Dict]:
        result = list()
        for item in objects:
            if type(item) in CLASSES_BASE.values():
                result.append(item.to_dict())
        return result

    def from_list_of_dicts(self, data_list: List[Dict]) -> List:
        result = list()
        for item in data_list:
            new_object = CLASSES_BASE[item['classname']](self, self.game.controller)
            new_object.from_dict(item)
            result.append(new_object)
        return result

    def load(self):
        self.from_dict(self.game.file_manager.read_data(self.data_filename))

    def save(self):
        self.game.file_manager.write_data(self.data_filename, self.to_dict())
