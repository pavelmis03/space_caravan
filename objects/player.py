import math

import pygame

from objects.base import SpriteObject


class Player(SpriteObject):
    filename = 'images/player.png'
    controls = {
        'up': pygame.K_w,
        'down': pygame.K_s,
        'right': pygame.K_d,
        'left': pygame.K_a,
    }

    def __init__(self, game, x=400, y=400):
        super().__init__(game, Player.filename)
        self.resize(0.5)
        self.rect.centerx = x
        self.rect.centery = y
        self.x = x
        self.y = y
        self.rotation = 0
        self.rotated_image = self.image
        self.rotated_rect = self.rect

        self.window_width = self.game.width
        self.window_height = self.game.height
        self.speed = 4
        self.shift_x, self.shift_y = 0, 0

    def process_logic(self):
        if not (self.rect.left <= 0 and self.shift_x < 0) and not (self.rect.right >= self.window_width and self.shift_x > 0):
            self.rect.x += self.shift_x * self.speed
        if not (self.rect.top <= 0 and self.shift_y < 0) and not (self.rect.bottom >= self.window_height and self.shift_y > 0):
            self.rect.y += self.shift_y * self.speed

    def collision(self, other_ball):
        self.shift_x, other_ball.shift_x = other_ball.shift_x, self.shift_x
        self.shift_y, other_ball.shift_y = other_ball.shift_y, self.shift_y

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.keyup(event.key)
        if event.type == pygame.KEYUP:
            self.keydown(event.key)
        if event.type == pygame.MOUSEMOTION:
            self.mousemotion()

    def process_draw(self):
        #self.rotated_image = pygame.transform.rotate (self.image, -self.rotation)
        self.rotated_rect = self.rotated_image.get_rect(center=(self.rect.centerx, self.rect.centerx))

        self.game.screen.blit(self.rotated_image, self.rotated_rect)

    def keyup(self, key):
        if key == Player.controls['up']:
            self.shift_y -= 1
        if key == Player.controls['down']:
            self.shift_y += 1
        if key == Player.controls['left']:
            self.shift_x -= 1
        if key == Player.controls['right']:
            self.shift_x += 1

    def keydown(self, key):
        if key == Player.controls['up']:
            self.shift_y += 1
        if key == Player.controls['down']:
            self.shift_y -= 1
        if key == Player.controls['left']:
            self.shift_x += 1
        if key == Player.controls['right']:
            self.shift_x -= 1

    def mousemotion(self):
        pos = pygame.mouse.get_pos()

        self.rotation = 180 * (math.atan2(self.rect.centery - pos[1], pos[0] - self.rect.centerx) / math.pi)
        self.rotated_image = pygame.transform.rotate (self.image, self.rotation)
        self.rotated_rect = self.rotated_image.get_rect (center=(self.rect.centerx, self.rect.centerx))
        # here's rotation