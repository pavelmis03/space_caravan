from controller.controller import Controller
from drawable_objects.drop.base import Drop
from geometry.point import Point
from random import randint


class AmmoDrop(Drop):
    IMAGE_NAME = 'other.ammo'

    def __init__(self, scene, controller: Controller,
                 pos: Point, angle: float = 0, zoom: float = 0.15, usage_radius: float = 42):
        super().__init__(scene, controller, pos, angle, zoom, usage_radius)

    def process_logic(self):
        self._update_player_nearby()
        if self.player_nearby:
            self.activate()
            self.destroy()

    def activate(self):
        MINIMUM_AMMO = 1
        MAXIMUM_AMMO = 5
        ammo_cnt = randint(MINIMUM_AMMO, MAXIMUM_AMMO)
        for key in self.scene.player.ammo:
            self.scene.player.ammo[key] += ammo_cnt
