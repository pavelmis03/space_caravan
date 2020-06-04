from drawable_objects.base import Animation
from random import randrange

from geometry.point import Point
from geometry.segment import Segment
from geometry.vector import vector_from_length_angle


def create_particles(enemy, damage, pos, angle):
    if damage < 50:
        amount = randrange(4, 6)
    elif damage < 100:
        amount = randrange(6, 10)
    else:
        amount = randrange(12, 17)
    for _ in range(amount):
        enemy.scene.game_objects.append(Particle(enemy, pos, angle))


class Particle(Animation):

    IMAGE_NAMES = [
        'moving_objects.particles.particle23',
        'moving_objects.particles.particle22',
        'moving_objects.particles.particle21',
    ]
    SECOND_TYPE_IMAGE = 'moving_objects.particles.particle24'

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
            intersection_point = self.scene.grid.intersect_seg_walls(tragectory)
            if intersection_point is not None:
                self.pos = intersection_point
                self.animation_end()
            else:
                self.move(next_pos)
                super().process_logic()

    def animation_end(self):
        type = randrange(0, 100)
        if type >= 70:
            self.image_name = self.SECOND_TYPE_IMAGE
            self.angle = randrange(0, 314)/100
        else:
            self.image_name = self.IMAGE_NAMES[2]
            self.zoom *= 2
        self.direction = Point(0, 0)