from typing import Dict
from drawable_objects.drop.base import Drop
from controller.controller import Controller
from geometry.point import Point
from weapons.weapons import WEAPON_VOCABULARY, weapon_to_dict
from random import randint


class WeaponDrop(Drop):
    IMAGE_NAME = 'other.gun' #временное значение. будет изменено в set_weapon_dict

    def __init__(self, scene, controller: Controller,
                 pos: Point, angle: float = 0, zoom: float = 0.5, usage_radius: float = 75):
        super().__init__(scene, controller,
                         pos, angle, zoom, usage_radius)
    # напиши нормальный get_image

    def activate(self):
        is_player_holding_fist = self.scene.player.weapon.__class__.__name__ == 'Fist'
        old_weapon = weapon_to_dict(self.scene.player.weapon)
        self.scene.player.set_weapon(self.__weapon_dict)
        self.destroy()

        if not is_player_holding_fist:  # если оружие игрка - кулаки(без оружия), ничего не дропнется
            new_weapon = WeaponDrop(self.scene, self.controller,
                                self.pos, self.angle, self.zoom, self.usage_radius)
            new_weapon.set_weapon_dict(old_weapon)
            self.scene.game_objects.append(new_weapon)

    def set_weapon_dict(self, weapon_dict: Dict):
        self.__weapon_dict = weapon_dict
        self.image_name = WEAPON_VOCABULARY[self.__weapon_dict['weapon']].IMAGE_NAME

    def to_dict(self) -> Dict:
        result = super().to_dict()
        result.update(self.__weapon_dict)
        return result

    def from_dict(self, data_dict: Dict):
        super().from_dict(data_dict)

        weapon_dict = {'weapon': data_dict['weapon']}
        if 'magazine' in data_dict:
            weapon_dict.update({'magazine': data_dict['magazine']})

        self.set_weapon_dict(weapon_dict)


class MedKitDrop(Drop):
    IMAGE_NAME = 'other.medkit'

    def __init__(self, scene, controller: Controller,
                 pos: Point, angle: float = 0, zoom: float = 0.15, usage_radius: float = 75):
        POS_TRANSITION = Point(0, -10)
        super().__init__(scene, controller,
                         (pos + POS_TRANSITION), angle, zoom, usage_radius)

    def activate(self):
        self.scene.player.hp = self.scene.player.MAXHP
        self.destroy()

class EssenceDrop(Drop):
    IMAGE_NAME = 'other.essence'

    def __init__(self, scene, controller: Controller,
                 pos: Point, angle: float = 0, zoom: float = 0.15, usage_radius: float = 75):
        super().__init__(scene, controller,
                         pos, angle, zoom, usage_radius)

    def activate(self):
        self.scene.common_data.essence += 1
        self.destroy()


class FuelDrop(Drop):
    IMAGE_NAME = 'other.fuel'

    def __init__(self, scene, controller: Controller,
                 pos: Point, angle: float = 0, zoom: float = 0.25, usage_radius: float = 75):
        super().__init__(scene, controller,
                         pos, angle, zoom, usage_radius)

    def activate(self):
        MINIMUM_ADD = 75
        MAXIMUM_ADD = 125
        self.scene.common_data.fuel += randint(MINIMUM_ADD, MAXIMUM_ADD)
        self.destroy()


def create_drop(name: str, scene, controller: Controller, pos: Point) -> Drop:
    """
    создать новый дроп по названию name
    """
    if name in WEAPON_VOCABULARY:
        tmp_weapon = WEAPON_VOCABULARY[name](scene.player)
        res = WeaponDrop(scene, controller, pos)
        res.set_weapon_dict(weapon_to_dict(tmp_weapon))
        return res

    OTHER_DROP = {
        'MedKit': MedKitDrop,
        'Essence': EssenceDrop,
        'Fuel': FuelDrop
    }
    return OTHER_DROP[name](scene, controller, pos)

