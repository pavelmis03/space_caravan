from controller.controller import Controller
from drawable_objects.usable_object import UsableObject
from geometry.point import Point


class Drop(UsableObject):
    IMAGE_NAME = ''
    def __init__(self, scene, controller: Controller,
                 pos: Point, angle: float = 0, zoom: float = 0.5, usage_radius: float = 100):
        super().__init__(scene, controller, self.IMAGE_NAME,
                         pos, angle, zoom, usage_radius)