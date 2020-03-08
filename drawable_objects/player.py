import math

import pygame

from drawable_objects.base import GameSprite
from geometry.point import Point
from constants import DIRECTIONS

from scenes.base import Scene
from controller.controller import Controller

class Player(GameSprite):
    """
    Игрок на уровне (далек от завершения).

    :param scene: сцена, на которой находится игрок
    :param controller: контроллер
    :param pos: начальная позиция игрока
    :param angle: начальный угол поворота игрока
    """

    FILENAME = 'player'
    CONTROLS = [
        pygame.K_d,
        pygame.K_w,
        pygame.K_a,
        pygame.K_s,
    ]
    SPEED = 50

    def __init__(self, scene: Scene, controller: Controller, pos: Point,
                 angle: float = 0, resize_percents: float = 0.5):
        super().__init__(scene, controller, Player.FILENAME, pos, angle, resize_percents)

    @property
    def next_step_pos(self):
        velocity = Point(0, 0)
        for i in range(4):
            if self.controller.is_key_pressed(Player.CONTROLS[i]):
                velocity += DIRECTIONS[i]

        return self.pos + velocity * Player.SPEED
    def process_logic(self):
        screen_center = self.scene.game.center

        vector_to_mouse = self.controller.get_mouse_pos() - screen_center
        self.angle = math.atan2(-vector_to_mouse.y, vector_to_mouse.x)

        self.move(self.next_step_pos)