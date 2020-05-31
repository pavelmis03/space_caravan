from typing import Dict

from controller.controller import Controller
from drawable_objects.usable_object import UsableObject
from geometry.point import Point
from scenes.base import Scene


class CloneCapsule(UsableObject):
    IMAGE_ZOOM = 0.8

    def __init__(self, scene: Scene, controller: Controller, pos: Point, angle: float = 0):
        super().__init__ (scene, controller, 'level_objects.terminal_up',
                           pos, angle, self.IMAGE_ZOOM)
        self.spacemap_created = False

    def to_dict(self) -> Dict:
        result = super().to_dict()
        result.update ({
            'spacemap_created': self.spacemap_created,
        })
        return result

    def from_dict(self, data_dict: Dict):
        super().from_dict (data_dict)
        self.spacemap_created = data_dict['spacemap_created']

    def activate(self):
        pass
