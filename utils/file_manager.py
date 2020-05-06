import os
import shutil
import json

from typing import Dict


class FileManager:
    STORAGE_NAME = 'game_data'

    def __init__(self):
        if not os.path.exists(FileManager.STORAGE_NAME):
            os.mkdir(FileManager.STORAGE_NAME)
        os.chdir(FileManager.STORAGE_NAME)
        self.__root = os.path.abspath(os.path.curdir)

    def reset(self):
        os.chdir(self.__root)

    def create_space_storage(self, space_name: str):
        self.delete_space_storage(space_name)
        os.mkdir(space_name)
        self.enter_space_storage(space_name)

    def enter_space_storage(self, space_name: str):
        os.chdir(space_name)

    def delete_space_storage(self, space_name: str):
        if os.path.exists(space_name):
            shutil.rmtree(space_name)

    def read_data(self, file_name: str) -> Dict:
        file = open(file_name, 'r')
        data_str = file.read()
        file.close()
        data_dict = json.loads(data_str)
        return data_dict

    def write_data(self, file_name: str, data_dict: Dict):
        data_str = json.dumps(data_dict, sort_keys=True, indent=2)
        file = open(file_name, 'w')
        file.write(data_str)
        file.close()
