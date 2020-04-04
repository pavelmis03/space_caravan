from weapons.base import Weapon
from drawable_objects.bullet import Bullet
from geometry.vector import vector_from_length_angle
from geometry.point import Point


class Pistol(Weapon):

    def __init__(self, shooter):
        super().__init__(shooter)
        self.cooldown_time = 10

    def attack(self, pos: Point, angle: float):
        self.cooldown = self.cooldown_time
        self.is_working = False
        pos = pos + vector_from_length_angle(self.length, angle)
        bullet = Bullet(self.scene, self.controller, pos, angle)
        self.scene.game_objects.append(bullet)