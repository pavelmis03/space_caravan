import pygame

from typing import Dict

from geometry.point import Point
from controller.controller import Controller
from scenes.base import Scene
from drawable_objects.base import GameSprite
from geometry.distances import dist
from drawable_objects.popping_e import PoppingE
from utils.timer import Timer


class UsableObject(GameSprite):
    """
    Базовый класс объекта, с которым игрок может взаимодействовать на клавишу ACTIVATION_KEY,
    подойдя на определенное расстояние.
    """
    ACTIVATION_KEY = pygame.K_e
    ACTIVATION_COOLDOWN = 10

    def __init__(self, scene: Scene, controller: Controller, image_name: str, pos: Point, angle: float = 0,
                 zoom: float = 1, usage_radius: float = 100):
        super().__init__(scene, controller, image_name, pos, angle, zoom)
        self.usage_radius = usage_radius
        self.player_nearby = False
        self.popping_e = PoppingE(
            self.scene, self.controller, image_name, zoom)

    def activate(self):
        pass

    def process_logic(self):
        self.player_nearby = dist(
            self.scene.player.pos, self.pos) <= self.usage_radius
        if self.player_nearby:
            self.player_nearby = True
            pass
        if self._can_be_activated and self.player_nearby \
                and self.controller.is_key_pressed(key=UsableObject.ACTIVATION_KEY) and \
                self.scene.e_timer.is_alarm: #перезарядка на кнопку, чтобы избежать вечных циклов
            self.activate()
            self.scene.e_timer = Timer(UsableObject.ACTIVATION_COOLDOWN)
            self.scene.e_timer.start()

        self.popping_e.update_pos(self.pos)

    def process_draw(self):
        super().process_draw()
        self._popping_e_draw()

    def _popping_e_draw(self):
        if self.player_nearby:
            self.popping_e.process_draw()

    def destroy(self):
        self.popping_e.destroy()
        super().destroy()

    @property
    def _can_be_activated(self):
        return True