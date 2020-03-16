import math

import pygame

from controller.controller import Controller
from drawable_objects.base import Humanoid
from geometry.point import Point
from scenes.base import Scene


class Bullet(Humanoid):

    IMAGE_ZOOM = 0.3

    def direction_calculation(self, angle: float):
        x_speed = math.cos(angle) * self.speed
        y_speed = -math.sin(angle) * self.speed
        return Point(x_speed, y_speed)


    def __init__(self, scene: Scene, controller: Controller, pos: Point, angle: float = 0):
        self.speed = 10
        self.direction = self.direction_calculation(angle)
        self.livetime = 100
        self.bullet_type = 'bullet'
        super().__init__ (scene, controller, self.bullet_type, pos, angle, Bullet.IMAGE_ZOOM)


    def process_logic(self):
        self.move(self.pos + self.direction)
        self.livetime -= 1
        if (self.livetime == 0):
            self.destroy()
            pass

    def collision(self):
        pass