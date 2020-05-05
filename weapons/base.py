import pygame

from constants.mouse_buttons import MouseButtonID
from drawable_objects.base import AbstractObject
from geometry.point import Point
from geometry.segment import Segment
from geometry.vector import vector_from_length_angle
from utils.sound import SoundManager


class Weapon(AbstractObject):
    MAIN_BUTTON = MouseButtonID.LEFT
    ALTERNATIVE_BUTTON = MouseButtonID.RIGHT

    def __init__(self, attacker, cooldown_time, is_automatic = 0, type ='test'):
        """
        :param attacker: DrawableObject, имеющий оружие -> DrawableObject
        :param cooldown_time: Время между выстрелами -> int
        :param is_automatic: Автоматическое ли оружие -> bool
        :param type: Вид оружия(на всякий случай, может что-то с этим придумаем) -> string
        """
        super().__init__(attacker.scene, attacker.controller)
        self.is_working = True
        self.is_automatic = is_automatic
        self.is_attacking = False
        self.cooldown_time = cooldown_time
        self.cooldown = 0
        self.type = type

    def process_logic(self):
        if self.cooldown:
            self.cooldown -= 1
            if self.cooldown == 0:
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
        Что происходит при нажатии кнопки главной атаки(лев. кнопки мыши)
        """
        self.cooldown = self.cooldown_time
        self.is_attacking = self.is_automatic
        self.is_working = False

    def alternative_button_click(self):
        """
        Что происходит при нажатии кнопки дополнительной атаки(прав. кнопки мыши)
        """
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
    RELOAD_KEY = pygame.K_r

    def __init__(self, attacker, ammo, cooldown_time, reload_time, magazine_size, is_automatic, length,
                 bullets_in_magazine, type):
        """
        :param attacker: DrawableObject, имеющий оружие -> DrawableObject
        :param cooldown_time: Время между выстрелами -> int
        :param ammo: Количество пуль
        :param reload_time: Время перезарядки
        :param magazine_size: Размер магазина
        :param is_automatic: Автоматическое ли оружие -> bool
        :param length: Длина ствола
        :param bullets_in_magazine: Сколько пуль в магазине на момент получения оружия
        :param type: Вид оружия(на всякий случай, может что-то с этим придумаем) -> string
        """
        super().__init__(attacker, cooldown_time, is_automatic, type)
        self.reload_time = reload_time
        self.is_reloading = 0
        self.barrel_length = attacker.HITBOX_RADIUS + 1 + length
        self.magazine_size = magazine_size
        self.magazine = bullets_in_magazine
        self.ammo = ammo
        self._is_fired_this_tick = False

    def reload(self):
        """
        Функция перезарядки
        """
        self.remains = self.magazine
        self.magazine = min(self.magazine_size, self.ammo)
        self.ammo -= (self.magazine - self.remains)
        self.is_working = False
        self.cooldown = self.reload_time
        self.is_reloading = self.reload_time
        pass

    def process_logic(self):
        self._is_fired_this_tick = False
        if self.is_reloading:
            self.is_reloading -= 1
        if self.controller.is_key_pressed(
                RangedWeapon.RELOAD_KEY) and not self.is_reloading and self.magazine < self.magazine_size:
            self.reload()
        super().process_logic()

    def main_button_click(self):
        """
        Что происходит при нажатии кнопки главной атаки(лев. кнопки мыши)
        """
        super().main_button_click()
        self._is_fired_this_tick = True
        pos = self.scene.player.pos
        angle = self.scene.player.angle
        end_of_the_barrel = pos + vector_from_length_angle(self.barrel_length, angle)
        if self.magazine == 0:
            self.reload()
            return
        self.magazine -= 1
        SoundManager.play_sound('weapon.shoot')
        if self.scene.grid.intersect_seg_walls(Segment(pos, end_of_the_barrel)) is None:
            self.attack(end_of_the_barrel, angle)

    @property
    def is_fired_this_tick(self):
        """
        Издало ли оружие звук в этот тик(чтобы Enemy слышали)
        """
        return self._is_fired_this_tick

class MeleeWeapon(Weapon):

    def __init__(self, attacker, cooldown_time, length, type):
        """
        :param attacker: DrawableObject, имеющий оружие -> DrawableObject
        :param cooldown_time: Время между взмахами -> int
        :param length: Длина клинка
        :param type: Вид оружия(на всякий случай, может что-то с этим придумаем) -> string
        """
        super().__init__(attacker, cooldown_time, type)
        self.barrel_length = attacker.HITBOX_RADIUS + 1 + length
        self._is_fired_this_tick = False

        self.ammo = 8
        self.magazine=8
        self.is_reloading = 0

    def process_logic(self):
        self._is_fired_this_tick = False
        super().process_logic()

    def main_button_click(self):
        """
        Что происходит при нажатии кнопки главной атаки(лев. кнопки мыши)
        """
        super().main_button_click()
        self._is_fired_this_tick = False
        pos = self.scene.player.pos
        angle = self.scene.player.angle
        end_of_the_barrel = pos + vector_from_length_angle(self.barrel_length, angle)
        SoundManager.play_sound('weapon.shoot')
        if self.scene.grid.intersect_seg_walls(Segment(pos, end_of_the_barrel)) is None:
            self.attack(end_of_the_barrel, angle)

    @property
    def is_fired_this_tick(self):
        """
        Издало ли оружие звук в этот тик(чтобы Enemy слышали)
        """
        return self._is_fired_this_tick
