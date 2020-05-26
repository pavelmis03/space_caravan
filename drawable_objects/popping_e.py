from drawable_objects.base import GameSprite
from geometry.point import Point

from scenes.base import Scene
from controller.controller import Controller
from geometry.distances import dist

from drawable_objects.player import Player
from utils.image import ImageManager


class PoppingE(GameSprite):
    """
    'E', всплывающая над объектами, которые можно использовать. Двигается за родительским объектом вызовами
    update_pos, висит над картинкой родительского объекта на постоянной высоте.
    """
    IMAGE_ZOOM = 0.05
    IMAGE_NAME = 'interface.poppingE'
    ANGLE = 0
    HEIGHT_ABOVE_PARENT = 25

    def __init__(self, scene: Scene, controller: Controller, parent_image_name: str, parent_zoom: float = 1):
        super().__init__(scene, controller, self.IMAGE_NAME,
                         Point(0, 0), self.ANGLE, self.IMAGE_ZOOM)
        self.parent_image_name = parent_image_name
        self.parent_zoom = parent_zoom
        self.parent_pos = Point(0, 0)

    def update_pos(self, parent_pos):
        self.parent_pos = parent_pos
        parent_image_height = ImageManager.get_height(self.parent_image_name, self.parent_zoom)
        self.move(parent_pos + Point(0, -parent_image_height / 2 - self.HEIGHT_ABOVE_PARENT))
