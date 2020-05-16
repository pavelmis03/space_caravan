import os
import shutil  # хех, шутки шутил
import json

from typing import Dict


class GameDataManager:
    """
    Менеджер файлов игры, в которых хранится информация о мирах.
    """

    STORAGE_ROOT = 'game_data'

    def __init__(self):
        if not os.path.exists(GameDataManager.STORAGE_ROOT):
            os.mkdir(GameDataManager.STORAGE_ROOT)
        os.chdir(GameDataManager.STORAGE_ROOT)
        self.__root = os.path.abspath(os.path.curdir)

    def reset(self):
        os.chdir(self.__root)

    def create_space_storage(self, space_name: str):
        """
        Создание хранилища файлов для нового игрового мира и перемещение в это хранилище.
        """
        self.delete_space_storage(space_name)
        os.mkdir(space_name)
        self.enter_space_storage(space_name)

    def enter_space_storage(self, space_name: str):
        os.chdir(space_name)

    def delete_space_storage(self, space_name: str):
        if os.path.exists(space_name):
            shutil.rmtree(space_name)

    def read_data(self, file_name: str) -> Dict:
        """
        Чтение словаря из файла в формате json.
        """
        file = open(file_name + '.json', 'r')
        data_str = file.read()
        file.close()
        data_dict = json.loads(data_str)
        return data_dict

    def write_data(self, file_name: str, data_dict: Dict):
        """
        Запись словаря в файл в формате json.
        """
        data_str = json.dumps(data_dict, sort_keys=True, indent=2)
        file = open(file_name + '.json', 'w')
        file.write(data_str)
        file.close()
