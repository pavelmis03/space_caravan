from weapons.base import RangedWeapon
from drawable_objects.bullet import Bullet
from geometry.point import Point
from random import randrange


class Pistol(RangedWeapon):

    DAMAGE = 100

    def __init__(self, owner, ammo, bullets_in_magazine=12):
        super ().__init__ (owner, ammo, bullets_in_magazine, magazine_size=12, main_attack_interval=12, reload_time=40,
                           bullet_type='Pistol')

    def shot(self, pos: Point, angle: float):
        bullet = Bullet(self.scene, self.controller, pos, angle, Pistol.DAMAGE)
        self.scene.game_objects.append(bullet)


class Shotgun(RangedWeapon):

    DAMAGE = 100

    def __init__(self, owner, ammo, bullets_in_magazine=6):
        super().__init__(owner, ammo, bullets_in_magazine, magazine_size=6, main_attack_interval=15, reload_time=80,
                         bullet_type='Shotgun')
        self.shells = 5

    def shot(self, pos: Point, angle: float):
        for i in range(self.shells):
            bullet = Bullet(self.scene, self.controller, pos, angle + float(randrange(-100, 100) / 600), Shotgun.DAMAGE)
            self.scene.game_objects.append(bullet)


class BurstFiringPistol(RangedWeapon):

    DAMAGE = 100

    def __init__(self, owner, ammo, bullets_in_magazine=20):
        super().__init__ (owner, ammo, bullets_in_magazine, magazine_size=20, main_attack_interval=15, reload_time=60,
                           bullet_type='Pistol', is_automatic=False, combo_attack_interval=3, combo_size=4)

    def shot(self, pos: Point, angle: float):
        bullet = Bullet(self.scene, self.controller, pos, float(angle + float(randrange(-100, 100) / 800)), BurstFiringPistol.DAMAGE)
        self.scene.game_objects.append(bullet)


class AutomaticRifle(RangedWeapon):

    DAMAGE = 100

    def __init__(self, owner, ammo, bullets_in_magazine=25):
        super().__init__ (owner, ammo, bullets_in_magazine, magazine_size=25, main_attack_interval=5, reload_time=60,
                           bullet_type='Rifle', is_automatic=True)

    def shot(self, pos: Point, angle: float):
        bullet = Bullet(self.scene, self.controller, pos, angle, AutomaticRifle.DAMAGE)
        self.scene.game_objects.append(bullet)
