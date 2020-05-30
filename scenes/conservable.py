from typing import Dict

from scenes.base import Scene


class ConservableScene(Scene):
    def __init__(self, game, data_filename: str):
        super().__init__(game)
        self.data_filename = data_filename

    def construct(self):
        if self.data_filename and self.game.file_manager.file_exists(self.data_filename):
            self.load()
        else:
            self.initialize()
            self.save()

    def initialize(self):
        pass

    def load(self):
        self.from_dict(self.game.file_manager.read_data(self.data_filename))

    def save(self):
        if self.data_filename:
            self.game.file_manager.write_data(self.data_filename, self.to_dict())

    def from_dict(self, data_dict: Dict):
        pass

    def to_dict(self) -> Dict:
        return {}
