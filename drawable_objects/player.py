import math

import pygame

from drawable_objects.base import GameSprite
from geometry.point import Point
from constants import DIRECTIONS


class Player(GameSprite):
    FILENAME = 'images/player.png'
    CONTROLS = [
        pygame.K_d,
        pygame.K_w,
        pygame.K_a,
        pygame.K_s,
    ]
    SPEED = 4

    def __init__(self, scene, controller, pos, angle):
        super().__init__(scene, controller, Player.FILENAME, pos, angle)
        self.resize(0.5)

    def process_logic(self):
        vector_to_mouse = self.controller.get_mouse_pos() - self.pos
        self.rotate(math.atan2(-vector_to_mouse.y, vector_to_mouse.x))

        velocity = Point(0, 0)
        for i in range(4):
            if self.controller.is_key_pressed(Player.CONTROLS[i]):
                velocity += DIRECTIONS[i]
        self.move(self.pos + velocity * Player.SPEED)
