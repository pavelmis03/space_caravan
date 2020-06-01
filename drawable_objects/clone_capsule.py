from typing import Dict

from controller.controller import Controller
from drawable_objects.base import GameSprite
from drawable_objects.usable_object import UsableObject
from geometry.point import Point
from scenes.base import Scene
from weapons.weapons import WEAPON_VOCABULARY


def transplant_soul_between_bodies(player, soulless_body):
    soulless_body.weapon.owner = player

    if player.weapon.type == 'Ranged':
        player.weapon.is_reloading = 0
        player.weapon.reload_request = False
    player.weapon.cooldown = 0
    player.weapon.burst = 0
    player.weapon_slots[player.weapon_slots_ind] = player.weapon
    player.change_weapon_request = -1
    player.change_weapon_cooldown = 0

    pos = player.pos
    player.move(soulless_body.pos)
    soulless_body.move(pos)
    player.angle, soulless_body.angle = soulless_body.angle, player.angle
    player.image_name, soulless_body.image_name = soulless_body.image_name, player.image_name
    player.zoom, soulless_body.zoom = soulless_body.zoom, player.zoom

    player.weapon_slots[0], soulless_body.weapon_slots[0] = soulless_body.weapon_slots[0], player.weapon_slots[0]
    player.weapon_slots[1], soulless_body.weapon_slots[1] = soulless_body.weapon_slots[1], player.weapon_slots[1]

    player.ammo['Pistol'], soulless_body.ammo['Pistol'] = soulless_body.ammo['Pistol'], player.ammo['Pistol']
    player.ammo['Rifle'], soulless_body.ammo['Rifle'] = soulless_body.ammo['Rifle'], player.ammo['Rifle']
    player.ammo['Shotgun'], soulless_body.ammo['Shotgun'] = soulless_body.ammo['Shotgun'], player.ammo['Shotgun']

    player.weapon_slots_ind, soulless_body.weapon_slots_ind = soulless_body.weapon_slots_ind, player.weapon_slots_ind

    soulless_body.weapon = soulless_body.weapon_slots[soulless_body.weapon_slots_ind]
    soulless_body.weapon.owner = soulless_body
    player.weapon = player.weapon_slots[player.weapon_slots_ind]

    player.is_clone = not player.is_clone


class CloneCapsule(UsableObject):
    IMAGE_ZOOM = 0.8

    def __init__(self, scene: Scene, controller: Controller, pos: Point, angle: float = 0):
        super().__init__(scene, controller, 'level_objects.terminal_up',
                         pos, angle, self.IMAGE_ZOOM)
        self.spacemap_created = False
        self.soulless_player = None
        self.is_clone_created = False
        self.changing_cooldown = 0

    def process_logic(self):
        super().process_logic()
        if self.changing_cooldown:
            self.changing_cooldown -= 1

    def activate(self):
        if not self.changing_cooldown:
            self.changing_cooldown = 30
            if not(self.scene.player.is_clone or self.is_clone_created):

                self.scene.player.weapon.cooldown = 0
                self.scene.player.weapon.burst = 0
                if self.scene.player.weapon.type == 'Ranged':
                    self.scene.player.weapon.is_reloading = 0
                    self.scene.player.weapon.reload_request = False
                self.scene.player.weapon_slots[self.scene.player.weapon_slots_ind] = self.scene.player.weapon

                self.scene.player.change_weapon_request = -1
                self.scene.player.change_weapon_cooldown = 0

                self.soulless_player = SoullessPlayer(self.scene.player)
                self.scene.game_objects.append(self.soulless_player)
                self.scene.player.ammo = {
                    'Pistol': 0,
                    'Shotgun': 0,
                    'Rifle': 0,
                }
                self.scene.player.weapon_slots = [
                    WEAPON_VOCABULARY['Fist'](self.scene.player),
                    WEAPON_VOCABULARY['Fist'](self.scene.player),
                ]
                self.scene.player.weapon = self.scene.player.weapon_slots[0]
                self.scene.player.is_clone = True
                self.is_clone_created = True
            else:
                transplant_soul_between_bodies(self.scene.player, self.soulless_player)


class SoullessPlayer(GameSprite):
    """
    Неуправляемое тело игрока после создания клона
    """

    def __init__(self, player):
        super().__init__(player.scene, player.controller, player.image_name, player.pos, player.angle, player.zoom)
        self.ammo = {
            'Pistol': player.ammo['Pistol'],
            'Shotgun': player.ammo['Shotgun'],
            'Rifle': player.ammo['Rifle'],
        }
        self.weapon_slots = [
            player.weapon_slots[0],
            player.weapon_slots[1],
        ]
        self.weapon_slots_ind = player.weapon_slots_ind
        self.weapon = self.weapon_slots[self.weapon_slots_ind]
        self.weapon.owner = self

    def process_draw(self):
        super().process_draw()
        self.weapon.process_draw()
