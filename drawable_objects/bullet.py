import math
import pygame
from drawable_objects.base import GameSprite
from geometry.point import Point
from geometry.distances import dist
from geometry.segment import Segment
from geometry.intersections import intersect_seg_rect
from scenes.base import Scene
from controller.controller import Controller


class Bullet(GameSprite):

    IMAGE_ZOOM = 0.7

    def direction_calculation(self, angle: float):
        x_speed = math.cos(angle) * self.speed
        y_speed = -math.sin(angle) * self.speed
        return Point(x_speed, y_speed)

    def __init__(self, scene: Scene, controller: Controller, pos: Point, angle: float = 0):
        self.speed = 150
        self.direction = self.direction_calculation(angle)
        self.bullet_type = 'bullet'
        super().__init__ (scene, controller, self.bullet_type, pos, angle, Bullet.IMAGE_ZOOM)

    def process_logic(self):
        next_pos = self.pos + self.direction
        self.collision_manager(next_pos)
        self.move(next_pos)

    def collision_manager(self, next_pos: Point):
        tragectory = Segment(self.pos, next_pos)
        collision_with_wall_point = self.is_colliding_with_walls(tragectory)
        if collision_with_wall_point:
            self.collision_with_wall(collision_with_wall_point)

    def collide_rects(self, tragectory: Segment, rects):
        min = 1000000000.0
        nearest_collision = None
        for rect in rects:
            intersection_point = intersect_seg_rect(tragectory, rect)
            if intersection_point and dist(self.pos, intersection_point) < min:
                min = dist(self.pos, intersection_point)
                nearest_collision = intersection_point
        return nearest_collision

    def is_colliding_with_walls(self, tragectory: Segment):
        current_pos_nearest_collision = self.collide_rects(tragectory, self.scene.grid.get_collision_rects_nearby(tragectory.p1))
        nearest_collision = None
        if current_pos_nearest_collision:
            nearest_collision = current_pos_nearest_collision
        else:
            middle_pos = Point((tragectory.p2.x + tragectory.p1.x) / 2, (tragectory.p2.y + tragectory.p1.y) / 2)
            middle_pos_nearest_collision = self.collide_rects(tragectory, self.scene.grid.get_collision_rects_nearby(middle_pos))
            if middle_pos_nearest_collision:
                nearest_collision = middle_pos_nearest_collision
            else:
                next_pos_nearest_collision = self.collide_rects (tragectory, self.scene.grid.get_collision_rects_nearby(tragectory.p2))
                if next_pos_nearest_collision:
                    nearest_collision = next_pos_nearest_collision
        return nearest_collision

    def is_colliding_with_entities(self):
        pass

    def collision_with_wall(self, collision_point):
        self.scene.game_objects.append(Collision_Point(self.scene, self.controller, collision_point, self.angle))
        self.destroy()

    def collision_with_entity(self):
        pass


class Collision_Point(Bullet):
    IMAGE_ZOOM = 0.5

    def __init__(self, scene: Scene, controller: Controller, pos: Point, angle: float = 0):
        self.speed = 0
        self.bullet_type = 'bullet'
        self.lifetime = 200
        angle = angle
        super().__init__(scene, controller, pos, angle)

    def process_logic(self):
        self.lifetime -= 1
        if (self.lifetime <= 0):
            self.destroy()
        pass
