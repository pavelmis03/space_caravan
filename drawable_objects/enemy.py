import math

import pygame

from controller.controller import Controller
from drawable_objects.base import Humanoid
from geometry.point import Point
from scenes.base import Scene


class Enemy(Humanoid):

    IMAGE_ZOOM = 0.3
    VISION_RADIUS = 25 * 50
    HEARING_RANGE = 30

    def __init__(self, scene: Scene, controller: Controller, pos: Point, angle: float = 0):
        ENEMY_TYPE = 'player'
        super().__init__ (scene, controller, ENEMY_TYPE, pos, angle, Enemy.IMAGE_ZOOM)
        self.speed = 1
        self.direction = Point(0, 0)

        self.is_see_player = False
        self.is_aggred = False

    def direction_calculation(self):
        x_speed = math.cos(self.angle) * self.speed
        y_speed = -math.sin(self.angle) * self.speed
        return Point(x_speed, y_speed)

    def recount_angle(self):
        vector_to_player = self.pos - self.scene.player.pos
        self.angle = math.atan2(vector_to_player.y, -vector_to_player.x)


    def process_logic(self):
        if self.is_see_player:
            self.recount_angle()
            print('I see you')
        self.scene.grid.set_enemy_in_arr(self)
        self.direction = self.direction_calculation()
        self.move(self.pos + self.direction)

    def process_draw(self):
        super().process_draw()
        p1 = self.pos - self.scene.relative_center
        p2 = self.scene.player.pos - self.scene.relative_center
        pygame.draw.line(self.scene.screen, (255, 0, 0), [p1.x, p1.y],
            [p2.x, p2.y], 5)

    def collision(self):
        pass