import math

import pygame

from controller.controller import Controller
from drawable_objects.base import Humanoid
from geometry.point import Point
from scenes.base import Scene


class Enemy(Humanoid):

    IMAGE_ZOOM = 0.3

    def direction_calculation(self):
        x_speed = math.cos(self.angle) * self.speed
        y_speed = -math.sin(self.angle) * self.speed
        return Point(x_speed, y_speed)

    def recount_angle(self):
        vector_to_player = self.pos - self.scene.player.pos
        self.angle = math.atan2(vector_to_player.y, -vector_to_player.x)

    def __init__(self, scene: Scene, controller: Controller, pos: Point, angle: float = 0):
        self.angle = angle
        self.speed = 1
        self.direction = self.direction_calculation()
        self.enemy_type = 'player'
        super().__init__ (scene, controller, self.enemy_type, pos, angle, Enemy.IMAGE_ZOOM)


    def process_logic(self):
        self.recount_angle()
        self.direction = self.direction_calculation()
        self.move(self.pos + self.direction)

    def collision(self):
        pass