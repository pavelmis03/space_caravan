from typing import List, Dict

from scenes.base import Scene
from drawable_objects.interface.pause_manager import PauseManager
from utils.game_plane import GamePlane
from geometry.point import Point
from drawable_objects.player import Player


def delete_destroyed(objects: List[any]):
    """
    быстрое удаление уничтоженных эл-тов (который not enabled).
    так как мы меняем местами удаляемый эл-т и делаем pop, работает за O(n)

    :param objects: список объектов
    """
    i = 0
    while i < len(objects):
        if not objects[i].enabled:
            objects[i], objects[-1] = objects[-1], objects[i]
            objects.pop()
            continue
        i += 1


class GameScene(Scene):
    """
    Класс игровой сцены, где помимо объектов интерфейса есть игровые объекты, игрок и сетка.
    :param game: игра, создающая сцену
    """
    SHIFT_SENSIVITY = 1 / 16

    def __init__(self, game):
        super().__init__(game)
        self.game_objects = []
        self.enemies = []
        self.relative_center = Point(0, 0)
        self.game_paused = False
        self.plane = GamePlane()
        self.pause_manager = PauseManager(self, self.game.controller)
        self.grid = None
        self.player = None

        self.load_player()
        self.interface_objects.append(self.pause_manager)
        self.game.controller.input_objects.append(self.player)
        self.game.controller.input_objects.append(self.pause_manager)

    def initialize(self):
        pass

    def from_dict(self):
        pass

    def to_dict(self) -> Dict:
        self.save_player()
        return dict()

    def load_player(self):
        self.player = Player(self, self.game.controller, Point(100, 100), 0)

    def save_player(self):
        pass

    def get_mouse_center_offset(self) -> Point:
        mouse_pos = self.game.controller.get_mouse_pos()
        mouse_pos -= Point(self.game.width / 2, self.game.height / 2)
        return mouse_pos * self.SHIFT_SENSIVITY

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
        self.relative_center = self.player.pos - self.game.screen_rectangle.center
        self.relative_center += self.get_mouse_center_offset()
        self.relative_center = self.grid.get_correct_relative_pos(self.relative_center)

    def delete_destroyed_objects(self):
        """
        быстрое удаление уничтоженных эл-тов (который not enabled).
        так как мы меняем местами удаляемый эл-т и делаем pop, работает за O(n)
        """
        delete_destroyed(self.game_objects)
        delete_destroyed(self.enemies)

    def process_all_logic(self):
        self.interface_logic()
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
