import os
import shutil  # хех, шутки шутил
import json

from typing import List, Dict
from constants.saving import CLASSES_BASE
from geometry.point import Point


class GameDataManager:
    """
    Менеджер файлов игры, в которых хранится информация о мирах.
    """

    STORAGE_ROOT = 'game_data'

    def __init__(self):
        if not os.path.exists(GameDataManager.STORAGE_ROOT):
            os.mkdir(GameDataManager.STORAGE_ROOT)
        self.__space_name = None
        self.__space_path = None

    def set_current_space(self, space_name):
        self.__space_name = space_name
        self.__space_path = os.path.join(self.STORAGE_ROOT, space_name)

    def create_space_storage(self):
        self.delete_space_storage()
        os.mkdir(self.__space_path)

    def delete_space_storage(self):
        if os.path.exists(self.__space_path):
            shutil.rmtree(self.__space_path)

    def __get_file_path(self, file_name) -> str:
        return os.path.join(self.__space_path, file_name + '.json')

    def read_data(self, file_name: str) -> Dict:
        """
        Чтение словаря из файла в формате json.
        """
        file_path = self.__get_file_path(file_name)
        file = open(file_path, 'r')
        data_str = file.read()
        file.close()
        data_dict = json.loads(data_str)
        return data_dict

    def write_data(self, file_name: str, data_dict: Dict):
        """
        Запись словаря в файл в формате json.
        """
        data_str = json.dumps(data_dict, sort_keys=True, indent=2)
        file_path = self.__get_file_path(file_name)
        file = open(file_path, 'w')
        file.write(data_str)
        file.close()

    def get_all_space_names(self) -> List[str]:
        files_and_folders = os.listdir(self.STORAGE_ROOT)
        folders = list()
        for name in files_and_folders:
            if os.path.isdir(os.path.join(self.STORAGE_ROOT, name)):
                folders.append(name)
        return folders


def to_list_of_dicts(objects: List) -> List[Dict]:
    result = list()
    for item in objects:
        if type(item) in CLASSES_BASE.values():
            result.append(item.to_dict())
    return result


def from_list_of_dicts(obj, data_list: List[Dict]) -> List:
    result = list()
    for item in data_list:
        new_object = CLASSES_BASE[item['classname']](
            obj, obj.game.controller, Point(0, 0))
        new_object.from_dict(item)
        result.append(new_object)
    return result


def to_2dimensional_list_of_dicts(objects: List[List]) -> List[List[Dict]]:
    result = list()
    for item in objects:
        result.append(to_list_of_dicts(item))
    return result


def from_2dimensional_list_of_dicts(obj, data_list: List[List[Dict]]) -> List[List]:
    result = list()
    for item in data_list:
        result.append(from_list_of_dicts(obj, item))
    return result
