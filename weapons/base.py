from drawable_objects.base import AbstractObject
from geometry.point import Point
from geometry.segment import Segment
from geometry.vector import vector_from_length_angle
from constants.mouse_buttons import MouseButtonID
import pygame


class Weapon(AbstractObject):

    MAIN_BUTTON = MouseButtonID.LEFT
    ALTERNATIVE_BUTTON = MouseButtonID.RIGHT
    RELOAD_KEY = pygame.K_r

    def __init__(self, shooter, ammo, cooldown_time, reload_time, magazine_size, is_automatic, barrel_length, bullets_in_magazine):
        super().__init__(shooter.scene, shooter.controller)
        self.is_working = True
        self.is_automatic = is_automatic
        self.is_firing = False
        self.cooldown_time = cooldown_time
        self.reload_time = reload_time
        self.is_reloading = 0
        self.cooldown = 0
        self.barrel_length = shooter.HITBOX_RADIUS + 1 + barrel_length
        self.magazine_size = magazine_size
        self.magazine = bullets_in_magazine
        self.ammo = ammo

    def reload(self):
        self.magazine = min(self.magazine_size, self.ammo)
        self.ammo -= self.magazine
        self.is_working = False
        self.cooldown = self.reload_time
        self.is_reloading = self.reload_time
        pass

    def process_logic(self):
        if self.cooldown:
            self.cooldown -= 1
            if self.cooldown == 0:
                self.is_working = True
        if self.is_reloading:
            self.is_reloading -= 1
        if self.controller.is_key_pressed(Weapon.RELOAD_KEY) and not self.is_reloading:
            self.reload()
        button = self.controller.get_click_button()
        self.is_firing = self.is_automatic and self.controller.is_mouse_pressed(Weapon.MAIN_BUTTON) and self.is_firing
        if (button == Weapon.MAIN_BUTTON or self.is_firing) and self.is_working:
            self.main_attack(self.scene.player.pos, self.scene.player.angle)
        if button == Weapon.ALTERNATIVE_BUTTON:
            self.alternative_attack()

    def main_attack(self, pos, angle):
        self.magazine -= 1
        if self.magazine < 0:
            self.reload()
            return
        self.cooldown = self.cooldown_time
        self.is_firing = self.is_automatic
        self.is_working = False
        end_of_the_barrel = pos + vector_from_length_angle(self.barrel_length, angle)
        if self.scene.grid.intersect_seg_walls(Segment(pos, end_of_the_barrel)) is None:
            self.attack(end_of_the_barrel, angle)

    def alternative_attack(self):
        pass

    def attack(self, pos: Point, angle: float):
        pass
