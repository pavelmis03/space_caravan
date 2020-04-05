from weapons.base import Weapon
from drawable_objects.bullet import Bullet
from geometry.point import Point
from drawable_objects.bullet import Collision_Point
from random import randrange


class Pistol(Weapon):

    def __init__(self, shooter, ammo, bullets_in_magazine=0):
        super().__init__(shooter, ammo, 12, 40, 12, False, 10, bullets_in_magazine, 'Pistol')

    def attack(self, pos: Point, angle: float):
        bullet = Bullet(self.scene, self.controller, pos, angle)
        self.scene.game_objects.append(bullet)
        self.type = 'Pistol'


class Shotgun(Weapon):

    def __init__(self, shooter, ammo, bullets_in_magazine=0):
        super().__init__(shooter, ammo, 15, 80, 6, False, 0, bullets_in_magazine, 'Shotgun')
        self.shells = 5

    def attack(self, pos: Point, angle: float):
        for i in range(self.shells):
            self.scene.game_objects.append(Bullet(self.scene, self.controller, pos, angle + float(randrange(-100, 100) / 600)))