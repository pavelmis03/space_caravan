"""
Базовый класс оружия
"""
from drawable_objects.base import AbstractObject
from geometry.point import Point
from geometry.segment import Segment
from geometry.vector import vector_from_length_angle
from constants.mouse_buttons import MouseButtonID
import pygame


class Weapon(AbstractObject):
    """
    Базовый класс оружия
    """
    MAIN_BUTTON = MouseButtonID['LEFT']
    ALTERNATIVE_BUTTON = MouseButtonID['RIGHT']

    def __init__(self, attacker, cooldown_time, is_automatic, weapon_type):
        super().__init__(attacker.scene, attacker.controller)
        self.is_working = True
        self.is_automatic = is_automatic
        self.is_attacking = False
        self.cooldown_time = cooldown_time
        self.recharge = 0
        self.type = weapon_type

    def process_logic(self):
        if self.recharge:
            self.recharge -= 1
            if self.recharge == 0:
                self.is_working = True
        self.is_attacking = self.is_automatic and self.controller.is_mouse_pressed(
            Weapon.MAIN_BUTTON) and self.is_attacking
        button = self.controller.get_click_button()
        if (button == Weapon.MAIN_BUTTON or self.is_attacking) and self.is_working:
            self.main_button_click()
        if button == Weapon.ALTERNATIVE_BUTTON:
            self.alternative_button_click()

    def main_button_click(self):
        """
        Действие по нажатию главной кнопки мышы
        (объявляется в глобальной переменной класса)
        """
        self.recharge = self.cooldown_time
        self.is_attacking = self.is_automatic
        self.is_working = False

    def alternative_button_click(self):
        """
        Действие по нажатию альтернативной кнопки мышы
        (объявляется в глобальной переменной класса)
        """
        pass

    def attack(self, pos: Point, angle: float):
        """
        Атака оружием
        будет переписан в классах-детях
        """
        pass


class RangedWeapon(Weapon):
    """
    Базовый класс дальнобойного оружия
    """
    RELOAD_KEY = pygame.K_r

    def __init__(self, attacker, ammo, recharge,
                 reload_time, magazine_size, is_automatic,
                 length, bullets_in_magazine, weapon_type):
        super().__init__(attacker, recharge, is_automatic, weapon_type)
        self.reload_time = reload_time
        self.is_reloading = 0
        self.barrel_length = attacker.HITBOX_RADIUS + 1 + length
        self.magazine_size = magazine_size
        self.magazine = bullets_in_magazine
        self.ammo = ammo

    def reload(self):
        self.magazine = min(self.magazine_size, self.ammo)
        self.ammo -= self.magazine
        self.is_working = False
        self.recharge = self.reload_time
        self.is_reloading = self.reload_time
        pass

    def process_logic(self):
        if self.is_reloading:
            self.is_reloading -= 1
        if self.controller.is_key_pressed(RangedWeapon.RELOAD_KEY) and \
                not self.is_reloading and \
                self.magazine < self.magazine_size:
            self.reload()
        super().process_logic()

    def main_button_click(self):
        super().main_button_click()
        pos = self.scene.player.pos
        angle = self.scene.player.angle
        self.magazine -= 1
        if self.magazine < 0:
            self.reload()
            return
        end_of_the_barrel = pos + vector_from_length_angle(self.barrel_length, angle)
        if self.scene.grid.intersect_seg_walls(Segment(pos, end_of_the_barrel)) is None:
            self.attack(end_of_the_barrel, angle)
