from typing import Dict

from scenes.base import Scene


class ConservableScene(Scene):
    """
    Базовый класс сохраняемой сцены. Основная структура сохранений содержится здесь. Чтобы перейти на сцену, нужно
    создать объект класса сцены и воспользоваться Game.set_scene. Никакие методы сцены дополнительно вызывать не
    требуется.

    :param game: игра, создающая сцену
    :param data_filename: имя файла, в который сохраняется сцена (расширение не указывать)
    """
    def __init__(self, game, data_filename: str):
        super().__init__(game)
        self.data_filename = data_filename

    def construct(self):
        """
        Конструирование сцены. Вызывается автоматически игрой при установке сцены текущей. Сцена сама выбирает,
        загружаться или инициализироваться.
        """
        if self.data_filename and self.game.file_manager.file_exists(self.data_filename):
            self.load()
        else:
            self.initialize()
            self.save()

    def initialize(self):
        """
        Инициализация - создание сцены с нуля.
        """
        pass

    def load(self):
        """
        Загрузка сцены из файла.
        """
        self.from_dict(self.game.file_manager.read_data(self.data_filename))

    def save(self):
        """
        Сохранение сцены в файл (если self.data_filename не None).
        """
        if self.data_filename:
            self.game.file_manager.write_data(self.data_filename, self.to_dict())

    def from_dict(self, data_dict: Dict):
        """
        Формирование сцены по словарю с ее данными.
        """
        pass

    def to_dict(self) -> Dict:
        """
        Представление данных сцены в виде словаря.
        """
        return {}
