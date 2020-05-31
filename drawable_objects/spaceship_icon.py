from math import pi, sin, cos

from drawable_objects.base import SpriteObject
from scenes.base import Scene
from controller.controller import Controller
from geometry.point import Point
from geometry.vector import vector_from_length_angle


class SpaceshipIcon(SpriteObject):
    IMAGE_NAME = 'spacemap.spaceship_icon'
    IMAGE_ZOOM = 0.1
    SPEED = 0.5

    def __init__(self, scene: Scene, controller: Controller, revolving_radius: float):
        super().__init__(scene, controller, self.IMAGE_NAME, Point(), 0, self.IMAGE_ZOOM)
        self.planet_pos = Point()
        self.revolving_radius = revolving_radius
        self.angle_speed = self.SPEED / self.revolving_radius

    def set_planet_pos(self, new_planet_pos):
        self.planet_pos = new_planet_pos

    def process_logic(self):
        self.angle += self.angle_speed
        if self.angle >= 2 * pi:
            self.angle -= 2 * pi
        self.move(self.planet_pos + vector_from_length_angle(self.revolving_radius, self.angle + pi / 2))
