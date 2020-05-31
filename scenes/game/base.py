from typing import Dict, List

from scenes.conservable import ConservableScene
from utils.game_data_manager import from_list_of_dicts, to_list_of_dicts
from space.common_game_data import CommonGameData


class GameScene(ConservableScene):
    """
    Базовый класс игровой сцены, то есть сцены игрового мира. Не обязательно содержит игрока и игровые объекты
    (например, карта планет), но обязательно - объект с общими данными игры.
    
    :param game: игра, создающая сцену
    :param data_filename: имя файла, в который сохраняется сцена (расширение не указывать)
    """

    def __init__(self, game, data_filename: str):
        super().__init__(game, data_filename)
        self.data_filename = data_filename
        self.common_data = None

    def load_common_data(self):
        """
        Загрузка объекта с общими данными игры.
        """
        self.common_data = CommonGameData(self)
        self.common_data.load()

    def save(self):
        super().save()
        self.common_data.save()

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
