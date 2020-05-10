import pygame

from drawable_objects.bullet import Bullet
from constants.mouse_buttons import MouseButtonID
from drawable_objects.base import AbstractObject
from geometry.point import Point
from geometry.segment import Segment
from geometry.vector import vector_from_length_angle
from utils.sound import SoundManager
from random import randrange


class Weapon(AbstractObject):
    MAIN_BUTTON = MouseButtonID.LEFT
    ALTERNATIVE_BUTTON = MouseButtonID.RIGHT

    def __init__(self, owner, main_attack_interval, is_automatic=False, combo_attack_interval=0, combo_size=1):
        """
        :param owner: DrawableObject, имеющий оружие -> DrawableObject
        :param main_attack_interval: Время между выстрелами -> int
        :param is_automatic: Автоматическое ли оружие -> bool
        :param combo_attack_interval: Интервал между выстрелами в очереди(0, если не стреляет очередями) -> int
        :param combo_size: Длина очереди(если не атакует очередями == 1)
        """
        super().__init__(owner.scene, owner.controller)
        self.owner = owner
        self.angle = owner.angle
        self.pos = owner.pos
        self.is_automatic = is_automatic
        self.main_attack_interval = main_attack_interval
        self.combo_attack_interval = combo_attack_interval
        self.combo = 0
        self.combo_size = combo_size
        self.cooldown = 0

        self.reload_request = False #используется только в RangedWeapon, нужна тут для работы Player._weapon_controls

    def process_logic(self):
        self.angle = self.owner.angle
        self.pos = self.owner.pos
        if self.cooldown:
            self.cooldown -= 1
        if self.combo != 0 and self.cooldown == 0:
            self.combo -= 1
            if self.combo == 0:
                self.cooldown = self.main_attack_interval
            else:
                self.cooldown = self.combo_attack_interval
            self.attack(self.pos, self.angle)

    def main_attack(self):
        if self.cooldown == 0 and self.combo == 0:
            self.combo = self.combo_size

    def alternative_attack(self):
        pass

    def attack(self, pos: Point, angle: float):
        """
        Функция атаки

        :param pos: откуда производится атака
        :param angle: под каким углом производится атака
        """
        pass

    @property
    def is_fired_this_tick(self):
        """
        Издало ли оружие звук в этот тик(чтобы Enemy слышали)
        """
        return False


class RangedWeapon(Weapon):

    def __init__(self, owner, ammo, bullets_in_magazine, magazine_size, main_attack_interval,
                 reload_time, bullet_type, accuracy, is_automatic=False, shells=1, combo_attack_interval=0, combo_size=1):
        """
        :param owner: DrawableObject, имеющий оружие -> DrawableObject
        :param main_attack_interval: Время между атаками(очередями) -> int
        :param ammo: Количесвто пуль
        :param cooldown_time: Время между выстрелами -> int
        :param reload_time: Время перезарядки
        :param magazine_size: Размер магазина
        :param is_automatic: Автоматическое ли оружие -> bool
        :param combo_size: Длина очереди(если не атакует очередями == 1)
        :param combo_attack_interval: Интервал между выстрелами в очереди(0, если не стреляет очередями) -> int
        :param bullets_in_magazine: Сколько пуль в магазине на момент получения оружия
        :param bullet_type: Вид оружия(на всякий случай, может что-то с этим придумаем) -> string
        :param accuracy: Точность оружия
        :param shells: Количество Bullet, вылетающих из оружия при одном выстреле
        """
        super().__init__(owner, main_attack_interval, is_automatic, combo_attack_interval, combo_size)
        self.reload_time = reload_time
        self.is_reloading = 0
        self.reload_request = False
        self.barrel_length = owner.HITBOX_RADIUS + 1
        self.magazine_size = magazine_size
        self.magazine = bullets_in_magazine
        self.ammo = ammo
        self.bullet_type = bullet_type
        self.accuracy = accuracy
        self.shells = shells
        self._is_fired_this_tick = False

    def reload(self):
        """
        Функция перезарядки
        """
        self.combo = 0
        if self.magazine == self.magazine_size or self.ammo == 0:
            self.reload_request = False
            return
        if not self.is_reloading:
            ammo_to_add = min(self.ammo, self.magazine_size - self.magazine)
            self.magazine += ammo_to_add
            self.ammo -= ammo_to_add
            self.cooldown = self.reload_time
            self.is_reloading = self.reload_time

    def process_logic(self):
        if self.is_reloading:
            self.is_reloading -= 1
            if not self.is_reloading:
                self.reload_request = False
        self._is_fired_this_tick = False
        super().process_logic()
        if self.reload_request and not self.is_reloading and self.combo == 0:
            self.reload()

    def attack(self, pos: Point, angle: float):
        if self.owner.__class__.__name__ == 'Player':
            self._is_fired_this_tick = True
        if self.magazine == 0:
            self.cooldown = 0
            self.reload()
            return
        self.magazine -= 1
        SoundManager.play_sound('weapon.shoot')
        end_of_the_barrel = self.owner.pos + vector_from_length_angle(self.barrel_length, self.angle)
        if self.scene.grid.intersect_seg_walls(Segment(self.owner.pos, end_of_the_barrel)) is None:
            self.shot(end_of_the_barrel, self.angle)

    def shot(self, pos: Point, angle: float):
        for i in range(self.shells):
            bullet = Bullet(self.scene, self.controller, pos,
                            angle + randrange(-100, 100) / (self.accuracy**2 - self.accuracy * 20 + 100), damage=100)
            self.scene.game_objects.append(bullet)

    @property
    def is_fired_this_tick(self):
        """
        Издало ли оружие звук в этот тик(чтобы Enemy слышали)
        """
        return self._is_fired_this_tick