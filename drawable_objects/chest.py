from typing import Dict
from drawable_objects.usable_object import UsableObject
from drawable_objects.drop.chest_drop import create_drop
from geometry.point import Point

from scenes.base import Scene
from controller.controller import Controller


class Chest(UsableObject):
    """
        Класс сундука, с которой игрок может взаимодействовать,
        при взаимодействии - не реализовано
        """
    IMAGE_ZOOM = 1.5
    IMAGE_NAME ='level_objects.boxes.box'
    USAGE_RADIUS = 80

    def __init__(self, scene: Scene, controller: Controller, pos: Point, angle: float = 0):
        super().__init__(scene, controller, Chest.IMAGE_NAME,
                         pos, angle, Chest.IMAGE_ZOOM, Chest.USAGE_RADIUS)
        self.__activated = False

    def activate(self):
        if self.__activated:
            return
        self.set_activated(True)

        drop = create_drop(self.__drop, self.scene, self.controller, self.pos)
        self.scene.game_objects.append(drop)

    def _popping_e_draw(self):
        if self.__activated:
            return
        super()._popping_e_draw()

    @property
    def _can_be_activated(self):
        return not self.__activated

    def from_dict(self, data_dict: Dict):
        super().from_dict(data_dict)
        self.set_activated(data_dict['activated'])
        self.set_drop(data_dict['drop'])

    def to_dict(self) -> Dict:
        res = super().to_dict()
        res.update({'drop': self.__drop})
        res.update({'activated': self.__activated})
        return res

    def set_drop(self, drop: str):
        self.__drop = drop

    def set_activated(self, is_activated: bool):
        self.__activated = is_activated
        if self.__activated:
            self.image_name = 'level_objects.boxes.box_open'
