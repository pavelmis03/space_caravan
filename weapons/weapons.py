from drawable_objects.slash import Slash
from weapons.base import RangedWeapon, MeleeWeapon
from drawable_objects.bullet import Bullet
from geometry.point import Point
from random import randrange


class Pistol(RangedWeapon):
    DAMAGE = 100

    def __init__(self, shooter, ammo, bullets_in_magazine=0):
        super().__init__(shooter, ammo, 12, 40, 12, False, 10, bullets_in_magazine, 'Pistol')

    def attack(self, pos: Point, angle: float):
        bullet = Bullet(self.scene, self.controller, pos, angle, Pistol.DAMAGE)
        self.scene.game_objects.append(bullet)


class Shotgun(RangedWeapon):

    DAMAGE = 100

    def __init__(self, shooter, ammo, bullets_in_magazine=0):
        super().__init__(shooter, ammo, 15, 80, 6, False, 0, bullets_in_magazine, 'Shotgun')
        self.shells = 5

    def attack(self, pos: Point, angle: float):
        for i in range(self.shells):
            self.scene.game_objects.append(Bullet(self.scene, self.controller, pos, angle + float(randrange(-100, 100) / 600), Shotgun.DAMAGE))

class Blade(MeleeWeapon):

    DAMAGE = 200

    def __init__(self, shooter):
        super().__init__(shooter, 15, 20,'Shotgun')

    def attack(self, pos: Point, angle: float):
        self.scene.game_objects.append(Slash(self.scene, self.controller, pos, angle, Blade.DAMAGE))

