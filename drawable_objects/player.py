import math

import pygame

from drawable_objects.base import Humanoid
from geometry.point import Point
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
    SPEED = 12

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
