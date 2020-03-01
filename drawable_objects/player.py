import math

import pygame

from drawable_objects.base import GameSprite
from geometry.basic_geometry import Point


class Player(GameSprite):
    FILENAME = 'images/player.png'
    CONTROLS = {
        'up': pygame.K_w,
        'down': pygame.K_s,
        'right': pygame.K_d,
        'left': pygame.K_a,
    }
    SPEED = 4

    def __init__(self, scene, controller, pos, angle):
        super().__init__(scene, controller, Player.FILENAME, pos, angle)
        self.resize(0.5)

        self.shift_x = 0
        self.shift_y = 0

    def process_logic(self):
        self.mousemotion()

        self.pos += Point(self.shift_x, self.shift_y) * self.SPEED

    def collision(self, other_ball):
        self.shift_x, other_ball.shift_x = other_ball.shift_x, self.shift_x
        self.shift_y, other_ball.shift_y = other_ball.shift_y, self.shift_y

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.keyup(event.key)
        if event.type == pygame.KEYUP:
            self.keydown(event.key)

    def keyup(self, key):
        if key == Player.CONTROLS['up']:
            self.shift_y -= 1
        if key == Player.CONTROLS['down']:
            self.shift_y += 1
        if key == Player.CONTROLS['left']:
            self.shift_x -= 1
        if key == Player.CONTROLS['right']:
            self.shift_x += 1

    def keydown(self, key):
        if key == Player.CONTROLS['up']:
            self.shift_y += 1
        if key == Player.CONTROLS['down']:
            self.shift_y -= 1
        if key == Player.CONTROLS['left']:
            self.shift_x += 1
        if key == Player.CONTROLS['right']:
            self.shift_x -= 1

    def mousemotion(self):
        pos = pygame.mouse.get_pos()

        self.rotate(math.atan2(-pos[1] + self.pos.y, pos[0] - self.pos.x))
        # here's rotation