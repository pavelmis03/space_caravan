import math

import pygame

from controller.controller import Controller
from drawable_objects.base import Humanoid
from geometry.point import Point
from scenes.base import Scene


class Enemy(Humanoid):

    IMAGE_ZOOM = 0.3
    VISION_RADIUS = 25 * 50
    HEARING_RANGE = 50

    def __init__(self, scene: Scene, controller: Controller, pos: Point, angle: float = 0):
        ENEMY_TYPE = 'player'
        super().__init__ (scene, controller, ENEMY_TYPE, pos, angle, Enemy.IMAGE_ZOOM)
        self.speed = 2#1
        self.direction = Point(0, 0)

        self.is_see_player = False
        self.is_aggred = False

        self.old_cell = (0, 0) #возможно временное решение

    @property
    def is_should_move(self):
        return self.is_aggred and not self.is_see_player

    def direction_calculation(self):
        x_speed = math.cos(self.angle) * self.speed
        y_speed = -math.sin(self.angle) * self.speed
        return Point(x_speed, y_speed)

    def recount_angle(self, new_pos):
        vector_to_player = self.pos - new_pos
        self.angle = math.atan2(vector_to_player.y, -vector_to_player.x)

    def interaction_with_player(self):
        if self.is_see_player:
            self.is_aggred = True
            new_pos = self.scene.player.pos
            self.recount_angle(new_pos)
            print('I see you')
            return
        if self.is_aggred:
            new_pos = self.scene.grid.get_pos_to_move(self)
            if new_pos is None:
                self.is_aggred = False
                return
            self.recount_angle(new_pos)
            print('Im going')

    def move_logic(self):
        self.interaction_with_player()
        if not self.is_should_move:
            return
        self.direction = self.direction_calculation()
        self.move(self.pos + self.direction)

    def process_logic(self):
        self.move_logic()
        self.scene.grid.set_enemy_in_arr(self)

    def process_draw(self):
        super().process_draw()
        p1 = self.pos - self.scene.relative_center
        p2 = self.scene.player.pos - self.scene.relative_center
        pygame.draw.line(self.scene.screen, (255, 0, 0), [p1.x, p1.y],
            [p2.x, p2.y], 5)

        if self.is_should_move:
            new_pos = self.scene.grid.get_center_of_cell_by_indexes(
                self.old_cell[0], self.old_cell[1])
            np = new_pos - self.scene.relative_center
            pygame.draw.circle(self.scene.screen, (0, 0, 255), (int(np.x), int(np.y)), 10)

    def collision(self):
        pass