from typing import Dict

from controller.controller import Controller
from drawable_objects.base import Humanoid
from drawable_objects.usable_object import UsableObject
from geometry.point import Point
from scenes.base import Scene
from weapons.weapons import WEAPON_VOCABULARY, weapon_to_dict


def transplant_soul_between_bodies(soulless_body):
    """
    Swap всех параметров игрока и неуправляемоо тела. Фактически подмена тела игрока на заданное

    :param soulless_body: тело, в которое перемещается игрок
    """
    player = soulless_body.scene.player

    player.hp, soulless_body.hp = soulless_body.hp, player.hp

    soulless_body.weapon_slots[0].owner = player
    soulless_body.weapon_slots[1].owner = player

    if player.weapon.type == 'Ranged':
        player.weapon.is_reloading = 0
        player.weapon.reload_request = False
    player.weapon.cooldown = 0
    player.weapon.combo = 0
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
    soulless_body.weapon_slots[0].owner = soulless_body
    soulless_body.weapon_slots[1].owner = soulless_body
    player.weapon = player.weapon_slots[player.weapon_slots_ind]

    player.is_clone = not player.is_clone


class CloneCapsule(UsableObject):
    """
    Капсула клонирования. Создаёт клона и позволяет меняться телами с клоном, если он уже создан
    """
    IMAGE_NAME = 'level_objects.clone'
    IMAGE_ZOOM = 0.38
    CLONE_COST = 3
    COOLDOWN_TIME = 30

    def __init__(self, scene: Scene, controller: Controller, pos: Point, angle: float = 0):
        super().__init__(scene, controller, self.IMAGE_NAME,
                         pos, angle, self.IMAGE_ZOOM)
        self.soulless_player = None
        self.is_clone_created = False
        self.changing_cooldown = 0

    def process_logic(self):
        super().process_logic()
        if self.changing_cooldown:
            self.changing_cooldown -= 1

    def activate(self):
        if not self.changing_cooldown:
            self.changing_cooldown = self.COOLDOWN_TIME

            if self.scene.player.weapon.__class__.__name__ == 'Knife':
                self.scene.player.image_name = 'moving_objects.player_with_knife'
                self.scene.player.weapon.animation_ind = -1
            elif self.scene.player.weapon.__class__.__name__ == 'Fist':
                self.scene.player.image_name = 'moving_objects.player_barehanded'

            if not(self.scene.player.is_clone or self.is_clone_created):
                if self.scene.common_data.essence >= CloneCapsule.CLONE_COST:
                    self.scene.common_data.essence -= CloneCapsule.CLONE_COST
                    self.scene.player.weapon.cooldown = 0
                    self.scene.player.weapon.combo = 0
                    if self.scene.player.weapon.type == 'Ranged':
                        self.scene.player.weapon.is_reloading = 0
                        self.scene.player.weapon.reload_request = False

                    self.scene.player.change_weapon_request = -1
                    self.scene.player.change_weapon_cooldown = 0

                    self.soulless_player = SoullessPlayer(self.scene.player)
                    self.scene.game_objects.append(self.soulless_player)

                    self.scene.player.hp = self.scene.player.MAXHP
                    self.scene.player.ammo = {
                        'Pistol': 100,
                        'Shotgun': 30,
                        'Rifle': 65,
                    }
                    self.scene.player.weapon_slots = [
                        WEAPON_VOCABULARY['Fist'](self.scene.player),
                        WEAPON_VOCABULARY['Fist'](self.scene.player),
                    ]
                    self.scene.player.weapon = self.scene.player.weapon_slots[0]

                    self.scene.player.is_clone = True
                    self.is_clone_created = True
            else:
                transplant_soul_between_bodies(self.soulless_player)

    def load_player_paremeters(self, player: Humanoid, data_dict: Dict):
        """
        Загрузка параметров неуправляемого игрока(клона или оригинала)

        :param player: неуправляемое тело
        :param data_dict: словарь, из которого происходит загрузка
        """
        new_pos = Point()
        new_pos.from_dict(data_dict['player_pos'])
        player.move(new_pos)
        player.angle = data_dict['player_angle']
        player.image_name = data_dict['player_image_name']
        player.zoom = data_dict['player_zoom']

        player.hp = data_dict['hp']

        player.weapon_slots[0].owner = self.scene.player
        player.weapon_slots[1].owner = self.scene.player

        player.ammo = data_dict['ammo']
        player.weapon_slots_ind = data_dict['weapon_slots_ind']

        player.weapon_slots = []
        for weapon_dict in data_dict['weapons']:
            weapon = WEAPON_VOCABULARY[weapon_dict['weapon']](player)
            if weapon.type == 'Ranged':
                weapon.magazine = weapon_dict['magazine']
            player.weapon_slots.append(weapon)
        player.weapon = player.weapon_slots[player.weapon_slots_ind]

    def from_dict(self, data_dict: Dict):
        super().from_dict(data_dict)
        self.is_clone_created = data_dict['is_clone_created']
        if self.is_clone_created:
            if self.scene.player.is_dead:
                self.is_clone_created = False
                self.scene.player.is_dead = False
                self.scene.player.is_clone = False
                self.load_player_paremeters(self.scene.player, data_dict)
            else:
                self.soulless_player = SoullessPlayer(self.scene.player)
                self.load_player_paremeters(self.soulless_player, data_dict)
                self.scene.game_objects.append(self.soulless_player)

    def to_dict(self) -> Dict:
        result = super().to_dict()
        result.update({'is_clone_created': self.is_clone_created})
        if self.is_clone_created:
            result.update({'player_pos': self.soulless_player.pos.to_dict()})
            result.update({'player_angle': self.soulless_player.angle})
            result.update({'player_image_name': self.soulless_player.image_name})
            result.update({'player_zoom': self.soulless_player.zoom})

            result.update({'hp': self.soulless_player.hp})

            weapons = []

            for item in self.soulless_player.weapon_slots:
                weapon_dict = weapon_to_dict(item)
                weapons.append(weapon_dict)

            result.update({'weapons': weapons})

            result.update({'weapon_slots_ind': self.soulless_player.weapon_slots_ind})
            result.update({'ammo': self.soulless_player.ammo})

        return result


class SoullessPlayer(Humanoid):
    """
    Неуправляемое тело игрока после создания клона
    """
    IMAGE_NAME = 'other.person-up_without_weapon'
    IMAGE_ZOOM = 0.25

    def __init__(self, player):
        super().__init__ (player.scene, player.controller, player.image_name, player.pos, player.angle, player.zoom)
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
        self.hp = player.hp

    def process_draw(self):
        super().process_draw()
        self.weapon.process_draw()
