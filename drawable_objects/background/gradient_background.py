"""
Неиспользуемый модуль. Может, позже пригодится.
"""
from drawable_objects.background.rgb import RGB
from drawable_objects.base import DrawableObject
from geometry.point import Point
from controller.controller import Controller
from scenes.base import Scene
from pygame import Surface, draw
from drawable_objects.background.transfusion_background import TransfusionBackground
from typing import List


def calc_radial_gradient(radius: int, center_color: RGB, out_color: RGB) -> Surface:
    """
    Линейно-круговой градиент на квадратной картинке
    """
    big_surface = Surface((2 * radius, 2 * radius)).convert_alpha()
    big_surface.fill((0, 0, 0, 0))
    ratio = 1.0 / radius
    r, g, b, a = (out_color - center_color).tuple
    r *= ratio
    g *= ratio
    b *= ratio
    a *= ratio

    for rad in range(radius, 0, -1):
        draw.circle(big_surface,
                    (center_color.r + int(r * rad),
                     center_color.g + int(g * rad),
                     center_color.b + int(b * rad),
                     center_color.a + int(a * rad)),
                    (radius, radius), rad)
    return big_surface


class GradientTransfusionBackground(DrawableObject):
    """
    Фон с круговым градиентом, центральный цвет которого
    переливается. Очень затратно по времени при больном радиусе.

    Готовый пример для тестирования:
    GradientTransfusionBackground(scene, controller, scene.width / 2,
                            [RGB(120, 0, 0), RGB(0, 120, 0), RGB(0, 0, 120)],
                            RGB(0, 0, 0))
    """

    def __init__(self, scene: Scene, controller: Controller, radius: float,
                 center_color: List[RGB], out_color: RGB):
        pos = scene.center
        pos -= Point(radius, radius)
        super().__init__(scene, controller, Point(pos.x, pos.y))

        self.out_color = out_color
        self.radius = int(radius)

        self.transfusion_background = TransfusionBackground(scene, controller, self.pos,
                                                            center_color)

    def process_logic(self):
        self.transfusion_background.process_logic()
        self.img = calc_radial_gradient(self.radius, self.transfusion_background.this_color,
                                        self.out_color)

    def process_draw(self):
        self.scene.screen.blit(self.img, (self.pos.x, self.pos.y))
