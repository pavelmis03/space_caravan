import math

import pygame

from controller.controller import Controller
from drawable_objects.base import Humanoid
from geometry.point import Point
from scenes.base import Scene

class EnemyCommand:
    def __init__(self, type: str, *params):
        self.type = type
        self.params = params

class Enemy(Humanoid):

    IMAGE_ZOOM = 0.3
    VISION_RADIUS = 25 * 50
    HEARING_RANGE = 50

    def __init__(self, scene: Scene, controller: Controller, pos: Point, angle: float = 0):
        ENEMY_TYPE = 'player'
        super().__init__ (scene, controller, ENEMY_TYPE, pos, angle, Enemy.IMAGE_ZOOM)
        self.speed = 2#1
        self.direction = Point(0, 0)

        self.is_has_command = False
        self.command = None
        self.is_aggred = False

        self.command_functions = {'move_to': self.command_move_to,
                                  'shoot': self.command_shoot}

    def direction_calculation(self):
        x_speed = math.cos(self.angle) * self.speed
        y_speed = -math.sin(self.angle) * self.speed
        return Point(x_speed, y_speed)

    def recount_angle(self, new_pos):
        vector_to_player = self.pos - new_pos
        self.angle = math.atan2(vector_to_player.y, -vector_to_player.x)

    def command_move_to(self, pos: Point):
        if pos == self.pos:
            self.is_has_command = False
            self.command_logic()
            return

        self.recount_angle(pos)
        self.direction = self.direction_calculation()
        self.move(self.pos + self.direction)

    def command_shoot(self):
        if not self.is_see_player:
            self.is_has_command = False
            self.command_logic()
            return
        self.recount_angle(self.scene.player.pos)

    def create_new_command(self):
        if self.is_see_player:
            self.is_aggred = True
            self.is_has_command = True
            self.command = EnemyCommand('shoot')
        elif self.is_aggred:
            new_pos = self.scene.grid.get_pos_to_move(self)
            if new_pos is None:
                self.is_aggred = False
                return
            self.is_has_command = True
            self.command = EnemyCommand('move_to', new_pos)

    def command_logic(self):
        if not self.is_has_command:
            self.create_new_command()

        if self.is_has_command:
            self.command_functions[self.command.type](*self.command.params)

    def process_logic(self):
        self.is_see_player = self.scene.grid.is_enemy_see_player(self)
        self.command_logic()

    def process_draw(self):
        super().process_draw()
        p1 = self.pos - self.scene.relative_center
        p2 = self.scene.player.pos - self.scene.relative_center
        pygame.draw.line(self.scene.screen, (255, 0, 0), [p1.x, p1.y],
            [p2.x, p2.y], 5)

        if self.is_has_command and self.command.type == 'move_to':
            new_pos = self.command.params[0]
            np = new_pos - self.scene.relative_center
            pygame.draw.circle(self.scene.screen, (0, 0, 255), (int(np.x), int(np.y)), 10)

    def collision(self):
        pass