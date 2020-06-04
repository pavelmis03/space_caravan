from drawable_objects.base import Animation
from random import randrange

from geometry.point import Point
from geometry.segment import Segment
from geometry.vector import vector_from_length_angle
from math import pi


def create_particles(enemy, damage, pos, angle):
    if damage < 50:
        amount = randrange(4, 6)
    elif damage < 100:
        amount = randrange(6, 10)
    else:
        amount = randrange(8, 12)
    for _ in range(amount):
        enemy.scene.game_objects.append(Particle(enemy, pos, angle))


class Particle(Animation):

    IMAGE_NAMES = [
        'moving_objects.particles.particle3',
        'moving_objects.particles.particle2',
        'moving_objects.particles.particle1',
    ]

    def __init__(self, bullet, pos, angle):
        self.angle = angle + randrange(-100, 100) / 100
        one_frame_vision_time = randrange(1, 2)
        super().__init__(bullet.scene, bullet.controller, pos, self.angle, one_frame_vision_time)
        self.zoom = randrange(17, 22) / 100
        speed = randrange(20, 60)
        self.direction = vector_from_length_angle(speed, self.angle)

    def process_logic(self):
        if self.direction != Point(0, 0):
            next_pos = self.pos + self.direction
            tragectory = Segment(self.pos, next_pos)
            if self.scene.grid.intersect_seg_walls(tragectory):
                self.animation_end()
            else:
                self.move(next_pos)
            super().process_logic()

    def animation_end(self):
        self.image_name = self.IMAGE_NAMES[2]
        self.direction = Point(0, 0)
        self.zoom *= 2