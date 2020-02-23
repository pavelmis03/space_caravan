import pygame
from random import randint

from objects.base import SpriteObject


class Player(SpriteObject):
    filename = 'images/player.png'

    def __init__(self, game, x=100, y=100):
        super().__init__(game, Player.filename)
        self.resize(0.5)
        self.rect.centerx = x
        self.rect.centery = y
        self.x = x
        self.y = y

        self.window_width = self.game.width
        self.window_height = self.game.height
        self.shift_x, self.shift_y = 0, 0

    def process_logic(self):
        self.rect.x += self.shift_x
        self.rect.y += self.shift_y
        if self.rect.left <= 0 or self.rect.right >= self.window_width:
            self.shift_x = 0
        if self.rect.top <= 0 or self.rect.bottom >= self.window_height:
            self.shift_y = 0

    def collision(self, other_ball):
        self.shift_x, other_ball.shift_x = other_ball.shift_x, self.shift_x
        self.shift_y, other_ball.shift_y = other_ball.shift_y, self.shift_y

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.shift_y = -1
            elif event.key == pygame.K_s:
                self.shift_y = 1
            if event.key == pygame.K_a:
                self.shift_x = -1
            elif event.key == pygame.K_d:
                self.shift_x = 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.shift_y = 0
            elif event.key == pygame.K_s:
                self.shift_y = 0
            if event.key == pygame.K_a:
                self.shift_x = 0
            elif event.key == pygame.K_d:
                self.shift_x = 0