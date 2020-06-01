from typing import Dict

from controller.controller import Controller
from drawable_objects.usable_object import UsableObject
from geometry.point import Point
from scenes.base import Scene
from weapons.weapons import WEAPON_VOCABULARY, WEAPON_ON_FLOOR_IMAGE


class WeaponShelf(UsableObject):

    IMAGE_NAME = 'level_objects.weapon_shelf'
    IMAGE_ZOOM = 1.15
    COOLDOWN_TIME = 20

    def __init__(self, scene: Scene, controller: Controller, pos: Point, angle: float = 0, weapon: str = None):
        super().__init__ (scene, controller, self.IMAGE_NAME,
                           pos, angle, self.IMAGE_ZOOM)
        self.HITBOX_RADIUS = 25 # для создания оружий
        if weapon is None:
            self.weapon = None
        else:
            self.weapon = WEAPON_VOCABULARY[weapon](self)
        self.changing_cooldown = 0
        self.usage_radius = 40

    def process_logic(self):
        super().process_logic()
        if self.changing_cooldown:
            self.changing_cooldown -= 1

    def process_draw(self):
        super().process_draw()
        if self.weapon is not None:
            self.weapon.process_draw()

    def activate(self):
        if not(self.changing_cooldown or
               (self.scene.player.weapon.__class__.__name__ == 'Fist' and self.weapon is None)):
            self.changing_cooldown = self.COOLDOWN_TIME
            self.scene.player.weapon.cooldown = 0
            self.scene.player.weapon.burst = 0
            if self.scene.player.weapon.type == 'Ranged':
                self.scene.player.weapon.reload_request = False
                self.scene.player.weapon.is_reloading = 0

            if self.weapon is None:
                self.weapon = self.scene.player.weapon
                self.weapon.owner = self
                self.weapon.angle = self.angle
                self.weapon.image_name = WEAPON_ON_FLOOR_IMAGE[self.weapon.__class__.__name__]
                self.scene.player.weapon_slots[self.scene.player.weapon_slots_ind] =\
                    WEAPON_VOCABULARY['Fist'](self.scene.player)
                self.scene.player.weapon = self.scene.player.weapon_slots[self.scene.player.weapon_slots_ind]

            elif self.scene.player.weapon.__class__.__name__ == 'Fist':
                self.weapon.image_name = WEAPON_VOCABULARY[self.weapon.__class__.__name__].IMAGE_NAME
                self.scene.player.weapon_slots[self.scene.player.weapon_slots_ind] = self.weapon
                self.scene.player.weapon = self.scene.player.weapon_slots[self.scene.player.weapon_slots_ind]
                self.scene.player.weapon.owner = self.scene.player
                self.weapon = None

            else:
                self.weapon.image_name = WEAPON_VOCABULARY[self.weapon.__class__.__name__].IMAGE_NAME
                weapon = self.weapon
                self.weapon = self.scene.player.weapon
                self.weapon.owner = self
                self.weapon.angle = self.angle
                self.weapon.image_name = WEAPON_ON_FLOOR_IMAGE[self.weapon.__class__.__name__]
                self.scene.player.weapon_slots[self.scene.player.weapon_slots_ind] = weapon
                self.scene.player.weapon = self.scene.player.weapon_slots[self.scene.player.weapon_slots_ind]
                self.scene.player.weapon.owner = self.scene.player

    def from_dict(self, data_dict: Dict):
        super().from_dict(data_dict)
        weapon = data_dict['weapon']
        if weapon is not None:
            self.weapon = WEAPON_VOCABULARY[weapon](self)
            self.weapon.image_name = WEAPON_ON_FLOOR_IMAGE[self.weapon.__class__.__name__]
            if self.weapon.type == 'Ranged':
                self.weapon.magazine = data_dict['weapon_magazine']
        else:
            self.weapon = None

    def to_dict(self) -> Dict:
        result = super().to_dict()
        if self.weapon is not None:
            result.update({'weapon': self.weapon.__class__.__name__})
            if self.weapon.type == 'Ranged':
                result.update({'weapon_magazine': self.weapon.magazine})
        else:
            result.update({'weapon': None})
        return result
