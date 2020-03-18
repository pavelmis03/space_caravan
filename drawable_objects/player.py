import math
import pygame

from typing import List

from drawable_objects.base import Humanoid
from geometry.point import Point
from geometry.vector import sign, length, normalized, cross_product
from geometry.rectangle import Rectangle
from geometry.circle import Circle
from geometry.intersections import intersert_circle_rect
from constants import DIRECTIONS, EPS
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
    SPEED = 12
    ACCURACY = 100

    def __init__(self, scene: Scene, controller: Controller, pos: Point, angle: float = 0):
        self.time = 0
        super().__init__(scene, controller, Player.IMAGE_NAME, pos, angle, Player.IMAGE_ZOOM)

    def process_logic(self):
        relative_center = self.scene.relative_center
        vector_to_mouse = self.controller.get_mouse_pos() + relative_center - self.pos
        self.angle = math.atan2(-vector_to_mouse.y, vector_to_mouse.x)

        velocity = Point(0, 0)

        if self.controller.get_click_button():
            self.scene.game_objects.append(Bullet(self.scene, self.controller, self.pos, self.angle))#'''
        '''self.time += 1
        self.scene.game_objects.append(Bullet(self.scene, self.controller, self.pos, self.angle))#''"
        if (self.time == 5):
            self.time = 0#'''

        if self in self.controller.input_objects:
            for i in range(4):
                if self.controller.is_key_pressed(Player.CONTROLS[i]):
                    velocity += DIRECTIONS[i]
            self.move(self.pos + velocity * Player.SPEED)

        for i in range(4):
            if self.controller.is_key_pressed(Player.CONTROLS[i]):
                velocity += DIRECTIONS[i]
        velocity *= Player.SPEED
        velocity = self.collide_walls(velocity)
        self.move(self.pos + velocity)

    def collide_rects(self, pos: Point, rects: List[Rectangle]) -> List[Point]:
        points = []
        for rect in rects:
            p = intersert_circle_rect(Circle(pos, Player.HITBOX_RADIUS), rect)
            if p:
                points.append(p)
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                if points[i] and points[j] and sign(length(points[i] - points[j])) == 0:
                    points[j] = None
        i = 0
        while i < len(points):
            if not points[i]:
                points[i], points[-1] = points[-1], points[i]
                points.pop()
            i += 1
        return points

    def get_velocity_edge(self, pos: Point, velocity: Point, rects: List[Rectangle]) -> (Point, Point):
        l = Point(0, 0)
        r = Point(velocity.x, velocity.y)
        for i in range(Player.ACCURACY):
            c = (l + r) / 2
            if len(self.collide_rects(pos + c, rects)) > 0:
                r = c
            else:
                l = c
        return l, r

    def collide_walls(self, velocity: Point) -> Point:
        if length(velocity) == 0:
            return velocity
        vel = Point(velocity.x, velocity.y)
        rects = self.scene.grid.get_collision_rects_nearby(self.pos)

        before_first, after_first = self.get_velocity_edge(self.pos, vel, rects)
        points = self.collide_rects(self.pos + after_first, rects)
        if len(points) == 0:
            return after_first
        if len(points) > 1:
            return before_first
        to_bump = normalized(points[0] + before_first - self.pos)
        proj_len = cross_product(vel - before_first, to_bump)
        new_vel = Point(to_bump.y, -to_bump.x) * proj_len
        before_second, after_second = self.get_velocity_edge(self.pos + before_first, new_vel, rects)
        points = self.collide_rects(self.pos + before_first + after_second, rects)
        if len(points) == 0:
            return before_first + before_second
        if len(points) > 0:
            return before_first + after_second
