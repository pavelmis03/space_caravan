from controller.controller import Controller
from drawable_objects.UsableObject import UsableObject
from geometry.point import Point
from scenes.base import Scene


class CloneCapsule(UsableObject):
    IMAGE_ZOOM = 0.8

    def __init__(self, scene: Scene, controller: Controller, pos: Point, angle: float = 0):
        super().__init__(scene, controller, 'level_objects.terminal_up',
                         pos, angle, CloneCapsule.IMAGE_ZOOM)

    def activate(self):
        pass
