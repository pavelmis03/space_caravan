from drawable_objects.usable_object import UsableObject
from controller.controller import Controller
from scenes.game.base import GameScene
from geometry.point import Point
from weapons.weapons import WEAPON_VOCABULARY, weapon_to_dict


class WeaponDrop(UsableObject):
    def __init__(self, scene: GameScene, controller: Controller, weapon_name: str,
                 pos: Point, angle: float = 0, zoom: float = 0.2, usage_radius: float = 100):
        tmp_weapon = WEAPON_VOCABULARY[weapon_name](scene.player)
        super().__init__(scene, controller, tmp_weapon.image_name, pos, angle, zoom, usage_radius)
        self.weapon_name = weapon_name

    def activate(self):
        old_weapon = weapon_to_dict(self.scene.player.weapon)['weapon']
        self.scene.player.set_weapon(self.weapon_name)
        self.enabled = False
        self.scene.game_objects.append(WeaponDrop(self.scene, self.controller, old_weapon,
                                        self.pos, self.angle, self.zoom, self.usage_radius))


def create_drop(name: str, scene: GameScene, controller: Controller, pos: Point,
                angle: float = 0, zoom: float = 0.5, usage_radius: float = 75) -> UsableObject:
    """
    создать новый дроп по названию name
    """
    if name in WEAPON_VOCABULARY:
        return WeaponDrop(scene, controller, name, pos, angle, zoom, usage_radius)

    raise Exception('Drop does not exist')
