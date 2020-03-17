from drawable_objects.background.rgb import RGB
from utils.image import ImageManager
from drawable_objects.base import SpriteObject
from geometry.point import Point
from controller.controller import Controller
from scenes.base import Scene
import pygame


def radial(radius, startcolor, endcolor):
    """
    Draws a linear raidal gradient on a square sized surface and returns
    that surface.
    """
    bigSurf = pygame.Surface((2 * radius, 2 * radius)).convert_alpha()
    bigSurf.fill((0, 0, 0, 0))
    dd = -1.0 / radius
    sr, sg, sb, sa = endcolor
    er, eg, eb, ea = startcolor
    rm = (er - sr) * dd
    gm = (eg - sg) * dd
    bm = (eb - sb) * dd
    am = (ea - sa) * dd

    draw_circle = pygame.draw.circle
    for rad in range(radius, 0, -1):
        draw_circle(bigSurf, (er + int(rm * rad),
                              eg + int(gm * rad),
                              eb + int(bm * rad),
                              ea + int(am * rad)), (radius, radius), rad)
    return bigSurf


class GradientBackground(SpriteObject):
    def __init__(self, scene: Scene, controller: Controller,
                 image_name: str, pos: Point,
                 start_color: RGB, final_color: RGB,
                 angle: float = 0, zoom: float = 1):
        pos.y -= (scene.game.width - scene.game.height) / 2
        # позиция смещается из-за того, что используется круг, а не эллипс
        super().__init__(scene, controller, image_name, pos, angle, zoom)
        self.start_color = start_color
        self.final_color = final_color
        
        self.img = radial(int(self.scene.game.width / 2), self.start_color.tuple, self.final_color.tuple)

    def process_draw(self):
        self.scene.screen.blit(self.img, (self.pos.x, self.pos.y))