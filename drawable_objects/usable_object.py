import pygame

from typing import Dict

from geometry.point import Point
from controller.controller import Controller
from scenes.base import Scene
from drawable_objects.base import GameSprite

from geometry.distances import dist
from math import cos
from math import sin

from drawable_objects.popping_e import PoppingE


class UsableObject(GameSprite):
    """
    Базовый класс объекта, с которым игрок может взаимодействовать на клавишу ACTIVATION_KEY,
    подойдя на определенное расстояние
    """
    ACTIVATION_KEY = pygame.K_e

    def __init__(self, scene: Scene, controller: Controller, image_name: str, pos: Point, angle: float = 0,
                 zoom: float = 1, usage_radius: float = 100):
        super().__init__(scene, controller, image_name, pos, angle, zoom)

        # Радиус вокруг объекта, в пределах которого с ним можно взаимодействовать
        self.usage_radius = usage_radius

        self.popping_e = PoppingE(
            self.scene, self.controller, self.pos, image_name, zoom, 0, usage_radius)
        # У каждого UsableObject есть своя PoppingE над ним
        self.scene.game_objects.append(self.popping_e)

    def from_dict(self, data_dict: Dict):
        super().from_dict(data_dict)
        self.popping_e.destroy()
        self.popping_e = PoppingE(
            self.scene, self.controller, self.pos, self.image_name, self.zoom, 0, self.usage_radius)
        self.scene.game_objects.append(self.popping_e)

    def process_logic(self):
        super().process_logic()
        if dist(self.scene.player.pos, self.pos) <= self.usage_radius:  # Проверка активации
            if self.controller.is_key_pressed(key=UsableObject.ACTIVATION_KEY):
                self.activate()

    def activate(self):
        """
        Функция, активирующаяся при взаимодействии с объектом
        """
        x_speed = cos(self.angle) * self.speed
        y_speed = -sin(self.angle) * self.speed
        return Point(x_speed, y_speed)

    def destroy(self):
        self.popping_e.destroy()
        super().destroy()
