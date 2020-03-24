import math
import pygame

from typing import List

from drawable_objects.base import Humanoid
from geometry.point import Point
from geometry.vector import sign, length, normalized
from geometry.distances import vector_dist_point_rect
from constants import DIRECTIONS
from scenes.base import Scene
from controller.controller import Controller


from drawable_objects.bullet import Bullet

class Player(Humanoid):
    """
    Игрок на уровне (далек от завершения).

    :param scene: сцена, на которой находится игрок
    :param controller: контроллер
    :param pos: начальная позиция игрока
    :param angle: начальный угол поворота игрока
    """

    IMAGE_NAME = 'player'
    IMAGE_ZOOM = 0.25
    CONTROLS = [
        pygame.K_d,
        pygame.K_w,
        pygame.K_a,
        pygame.K_s,
    ]
    SPEED = 3
    ACCURACY = 10

    def __init__(self, scene: Scene, controller: Controller, pos: Point, angle: float = 0):
        super().__init__(scene, controller, Player.IMAGE_NAME, pos, angle, Player.IMAGE_ZOOM)

    def process_logic(self):
        relative_center = self.scene.relative_center
        vector_to_mouse = self.controller.get_mouse_pos() + relative_center - self.pos
        self.angle = math.atan2(-vector_to_mouse.y, vector_to_mouse.x)

        velocity = Point(0, 0)

        if self.controller.get_click_button ():
            self.scene.game_objects.append(Bullet(self.scene, self.controller, self.pos, self.angle))

        if self in self.controller.input_objects:
            for i in range(4):
                if self.controller.is_key_pressed(Player.CONTROLS[i]):
                    velocity += DIRECTIONS[i]
            self.move(self.pos + velocity * Player.SPEED)

        for i in range(4):
            if self.controller.is_key_pressed(Player.CONTROLS[i]):
                velocity += DIRECTIONS[i]
        velocity *= Player.SPEED

        new_pos = self.go_from_walls(self.pos + velocity)
        if sign(length(new_pos - self.pos - velocity)) != 0:
            new_pos = self.go_from_walls(self.pos + velocity)
        self.move(new_pos)

    def go_from_walls(self, p: Point) -> Point:
        pos = Point(p.x, p.y)
        rects = self.scene.grid.get_collision_rects_nearby(pos)
        while True:
            v = []
            for rect in rects:
                current_v = vector_dist_point_rect(pos, rect)
                if sign(self.HITBOX_RADIUS - length(current_v)) == 1:
                    v.append(current_v)
            if len(v) == 0:
                break;
            for i in range(1, len(v)):
                if length(v[0]) > length(v[i]):
                    v[0], v[i] = v[i], v[0]
            push_v = normalized(v[0]) * (self.HITBOX_RADIUS - length(v[0]))
            pos += push_v
        return pos
