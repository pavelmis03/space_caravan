from typing import List
import pygame

from constants.color import COLOR
from geometry.point import Point


class Scene:
    """
    Базовый класс сцены.

    :param game: игра, создающая сцену
    """

    def __init__(self, game):
        self.game = game
        self.screen = self.game.screen
        self.interface_objects = []

    @property
    def width(self):
        return self.game.width

    @property
    def height(self):
        return self.game.height

    @property
    def center(self):
        return Point(self.width / 2, self.height / 2)

    def iteration(self):
        """
        Итерация работы сцены - обработка логики и отрисовка.
        """
        self.process_all_logic()
        self.process_all_draw()
        pygame.display.flip()  # double buffering
        pygame.time.wait(10)  # подождать 10 миллисекунд

    def process_all_logic(self):
        """
        Обработка логики сцены и ее объектов.
        """
        for item in self.interface_objects:
            item.process_logic()

    def process_all_draw(self):
        """
        Обработка отрисовки сцены и ее объектов.
        """
        self.screen.fill(COLOR['BLACK'])
        for item in self.interface_objects:
            item.process_draw()

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
    FIXED_CAMERA = False
    SHIFT_SENSIVITY = 1 / 40

    def __init__(self, game):
        super().__init__(game)
        self.game_objects = []
        self.enemies = []
        self.relative_center = Point(0, 0)
        self.grid = None
        self.player = None
        self.plane = None
        self.game_paused = False

    def interface_logic(self):
        """
        Логика недвижущихся на экране объектов
        """
        for item in self.interface_objects:
            item.process_logic()

    def game_logic(self):
        """
        Обработка логики в следующем порядке: сетка, игровые объекты, игрок.
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
        # смешение камеры к курсору мыши
        if not GameScene.FIXED_CAMERA:
            mouse_pos = self.game.controller.get_mouse_pos()
            mouse_pos -= Point(self.game.width / 2, self.game.height / 2)
            self.relative_center += mouse_pos * self.SHIFT_SENSIVITY

        self.relative_center = self.grid.get_correct_relative_pos(self.relative_center)

    def delete_destroyed_objects(self):
        """
        быстрое удаление уничтоженных эл-тов (который not enabled).
        так как мы меняем местами удаляемый эл-т и делаем pop, работает за O(n)
        """
        delete_destroyed(self.game_objects)
        delete_destroyed(self.enemies)

    def process_all_logic(self):
        """
        Логика всех объектов.
        """
        self.interface_logic()
        if not self.game_paused:
            self.game_logic()

        self.delete_destroyed_objects()

    def process_all_draw(self):
        """
        Отрисовка в следующем порядке: сетка, игровые объекты, игрок, объекты интерфейса.
        """
        self.screen.fill(COLOR['BLACK'])
        self.grid.process_draw()

        for item in self.game_objects:
            item.process_draw()
        for item in self.enemies:
            item.process_draw()

        self.player.process_draw()
        for item in self.interface_objects:
            item.process_draw()
