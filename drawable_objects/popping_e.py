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

    def __init__(self, scene: Scene, controller: Controller, pos: Point, parent_image: str, zoom: float = 1,
                 angle: float = 0, parent_radius: float = 0):
        self.parent_pos = pos  # позиция объекта, который может быть использован
        # радиус объекта, который может быть использован
        self.parent_radius = parent_radius

        pos += Point(0, -ImageManager.get_height(parent_image, zoom / 1.25))
        super().__init__(scene, controller, 'interface.poppingE',
                         pos, angle, PoppingE.IMAGE_ZOOM)

    def process_draw(self):
        if dist(self.scene.player.pos, self.parent_pos) <= self.parent_radius:
            super().process_draw()
