from controller.controller import Controller
from drawable_objects.base import GameSprite
from geometry.circle import Circle
from geometry.intersections import intersect_seg_circle
from geometry.point import Point
from geometry.segment import Segment
from geometry.vector import vector_from_length_angle, length
from scenes.base import Scene
from utils.image import ImageManager


def dist(p1: Point, p2: Point) -> float:
    """
    Расстояние между точками.

    :param p1: первая точка
    :param p2: вторая точка
    :return: числовое значение, или 10^8, если одной из точек нет
    """
    if p1 is None or p2 is None:
        return 100000000
    return length(p2 - p1)


class Slash(GameSprite):
    """
    Базовый удар ближним оружием (далек от завершения).

    :param scene: сцена, на которой находится анимация удара
    :param controller: контроллер
    :param pos: начальная позиция удара
    :param angle: начальный угол направления удара
    """

    IMAGE_ZOOM = 0.4
    IMAGE_NAME = 'moving_objects.melee_weapon.attack.heavy_splash.1'

    def __init__(self, scene: Scene, controller: Controller, pos: Point, angle: float, damage):
        super().__init__(scene, controller, Slash.IMAGE_NAME, pos, angle, Slash.IMAGE_ZOOM)
        self.direction = vector_from_length_angle(10, self.angle)
        self.damage = damage
        ImageManager.process_draw(
            'moving_objects.melee_weapon.attack.heavy_splash.1', self.pos, self.scene.screen, 1, self.angle)
        self.scene.game_objects.append(SlashAnimation(self.scene, self.controller, self.pos, self.angle))
        self.destroy()


class SlashAnimation(GameSprite):

    IMAGE_NAMES = [
        'moving_objects.melee_weapon.attack.heavy_splash.1',
        'moving_objects.melee_weapon.attack.heavy_splash.2',
        'moving_objects.melee_weapon.attack.heavy_splash.3',
    ]
    IMAGE_ZOOMS = [0.4, 0.4, 0.4]

    def __init__(self, scene: Scene, controller: Controller, pos: Point, angle: float = 0):
        pos = pos - vector_from_length_angle(8, angle)
        super().__init__(scene, controller, SlashAnimation.IMAGE_NAMES[0], pos, angle, SlashAnimation.IMAGE_ZOOMS[0])
        self.image_ind = 0
        self.one_frame_vision_time = 2

    def process_logic(self):
        self.image_name = SlashAnimation.IMAGE_NAMES[self.image_ind // self.one_frame_vision_time]
        self.zoom = SlashAnimation.IMAGE_ZOOMS[self.image_ind // self.one_frame_vision_time]
        self.image_ind += 1
        if self.image_ind >= len(SlashAnimation.IMAGE_NAMES) * self.one_frame_vision_time:
            self.destroy()
