from drawable_objects.base import GameSprite
from geometry.point import Point

from scenes.base import Scene
from controller.controller import Controller
from geometry.distances import dist

from drawable_objects.player import Player
from utils.image import ImageManager


class PoppingE(GameSprite):
    """
    'E', всплывающая над объектами, если их можно использовать
    """
    IMAGE_ZOOM = 0.05

    def __init__(self, scene: Scene, controller: Controller, pos: Point, angle: float = 0, parent_pos: Point = Point(0, 0), parent_radius: float = 0):
        pos += Point(0, -45)
        super().__init__(scene, controller, 'other.poppingE',
                         pos, angle, PoppingE.IMAGE_ZOOM)

        self.parent_pos = parent_pos #позиция объекта, который может быть использован
        self.parent_radius = parent_radius #радиус объекта, который может быть использован

    def process_logic(self):
        if dist (self.scene.player.pos, self.parent_pos) > self.parent_radius:
            self.destroy() #если игрок далеко, 'Е" уничтожается
