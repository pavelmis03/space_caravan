from typing import List, Dict

from drawable_objects.interface.pause_manager import PauseManager
from utils.game_plane import GamePlane
from geometry.point import Point
from drawable_objects.player import Player
from scenes.game.base import GameScene
from utils.camera import Camera
from utils.game_data_manager import from_list_of_dicts, to_list_of_dicts


def delete_destroyed(objects: List[any]):
    """
    Быстрое удаление уничтоженных эл-тов (который not enabled).
    Так как мы меняем местами удаляемый эл-т и делаем pop, работает за O(n).

    :param objects: список объектов
    """
    i = 0
    while i < len(objects):
        if not objects[i].enabled:
            objects[i], objects[-1] = objects[-1], objects[i]
            objects.pop()
            continue
        i += 1


class LevelScene(GameScene):
    """


    :param game: игра, создающая сцену
    :param data_filename: имя файла, в который сохраняется сцена (расширение не указывать)
    """
    FIXED_CAMERA = False
    PLAYER_SPAWN_POINT = Point(100, 100)

    def __init__(self, game, data_filename: str):
        super().__init__(game, data_filename)
        self.game_objects = []
        self.enemies = []
        self.relative_center = Point(0, 0)
        self.game_paused = False
        self.plane = GamePlane()
        self.grid = None
        self.player = None
        self.pause_manager = PauseManager(self, self.game.controller)
        self.interface_objects.append(self.pause_manager)
        self.camera = Camera(self)

    def to_dict(self) -> Dict:
        result = super().to_dict()
        result.update({
            'game_objects': to_list_of_dicts(self.game_objects),
            'enemies': to_list_of_dicts(self.enemies),
        })
        return result

    def from_dict(self, data_dict: Dict):
        super().from_dict(data_dict)
        self.game_objects += from_list_of_dicts(self,
                                                data_dict['game_objects'])
        self.enemies += from_list_of_dicts(self, data_dict['enemies'])

    def load_player(self):
        """
        Загрузка игрока (он хранится отдельно от сцен). Вызывается автоматически в Game.
        """
        self.player = Player(self, self.game.controller, Point(0, 0))
        self.player.load()
        self.player.move(self.PLAYER_SPAWN_POINT)

    def save(self):
        super().save()
        self.player.save()

    def game_logic(self):
        """
        Игровая логика в следующем порядке: сетка, игровые объекты и враги, игрок.
        """
        self.grid.process_logic()

        for item in self.game_objects:
            item.process_logic()
        for item in self.enemies:
            self.grid.save_enemy_pos(item.pos)
        for item in self.enemies:
            item.process_logic()

        self.player.process_logic()
        self.relative_center = self.camera.get_relative_center(
            not LevelScene.FIXED_CAMERA)

    def delete_destroyed_objects(self):
        """
        Удаление уничтоженных элементов.
        """
        delete_destroyed(self.game_objects)
        delete_destroyed(self.enemies)

    def process_all_logic(self):
        super().process_all_logic()
        if not self.game_paused:
            self.game_logic()

        self.delete_destroyed_objects()

    def game_draw(self):
        """
        Игровая отрисовка в следующем порядке: сетка, игровые объекты и враги, игрок.
        """
        self.grid.process_draw()

        for item in self.game_objects:
            item.process_draw()
        for item in self.enemies:
            item.process_draw()

        self.player.process_draw()

    def process_all_draw(self):
        self.clear_screen()
        self.game_draw()
        self.interface_draw()
