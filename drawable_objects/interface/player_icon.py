from controller.controller import Controller
from drawable_objects.base import SpriteObject
from drawable_objects.player import Player
from geometry.point import Point
from scenes.base import Scene
from utils.image import ImageManager


class PlayerIcon(SpriteObject):
    """
    Иконка игрока. Нужна для отображения хп игрока.
    меняет картинку в зависимоти от hp
    """
    IMAGES = [
        'interface.player_icon.state4',
        'interface.player_icon.state3',
        'interface.player_icon.state2',
        'interface.player_icon.state1',
    ]
    IMAGE_ZOOM = 0.5

    def __init__(self, scene: Scene, controller: Controller, player: Player):
        super().__init__(scene, controller, PlayerIcon.IMAGES[0], Point(
            0, 0), 0, PlayerIcon.IMAGE_ZOOM)
        self.player = player
        self.left_corner_to()

    def process_logic(self):
        hp_weight = self.player.MAXHP / len(PlayerIcon.IMAGES)
        index = int(self.player.hp / hp_weight)
        if index == len(PlayerIcon.IMAGES):
            index -= 1  # full hp
        self.image_name = PlayerIcon.IMAGES[index]

    def left_corner_to(self, pos: Point = 0):
        """
        Перемещает картинку так, что бы ее левый край
        был в точке pos
        :param pos: позиция перемещения
        """
        if not pos:
            pos = Point(0, 0)
        width = ImageManager.get_width(self.image_name, PlayerIcon.IMAGE_ZOOM)
        height = ImageManager.get_height(
            self.image_name, PlayerIcon.IMAGE_ZOOM)
        self.move(Point(width / 2, height / 2) + pos)
