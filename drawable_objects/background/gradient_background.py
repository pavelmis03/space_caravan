from drawable_objects.background.rgb import RGB
from drawable_objects.base import DrawableObject
from geometry.point import Point
from controller.controller import Controller
from scenes.base import Scene
from pygame import Surface, draw
from drawable_objects.background.transfusion_background import TransfusionBackground

def radial(radius, startcolor, endcolor):
    """
    Draws a linear raidal gradient on a square sized surface and returns
    that surface.
    """
    bigSurf = Surface((2 * radius, 2 * radius)).convert_alpha()
    bigSurf.fill((0, 0, 0, 0))
    dd = -1.0 / radius
    sr, sg, sb, sa = endcolor
    er, eg, eb, ea = startcolor
    rm = (er - sr) * dd
    gm = (eg - sg) * dd
    bm = (eb - sb) * dd
    am = (ea - sa) * dd

    draw_circle = draw.circle
    for rad in range(radius, 0, -1):
        draw_circle(bigSurf, (er + int(rm * rad),
                              eg + int(gm * rad),
                              eb + int(bm * rad),
                              ea + int(am * rad)), (radius, radius), rad)
    return bigSurf


class GradientBackground(DrawableObject):
    def __init__(self, scene: Scene, controller: Controller, pos: Point,
                 start_color: RGB, final_color: RGB):
        # позиция смещается из-за того, что используется круг, а не эллипс
        super().__init__(scene, controller, Point(pos.x, pos.y))
        #self.pos.y -= (scene.game.width - scene.game.height) / 2
        self.start_color = start_color
        self.final_color = final_color
        self.radius = int(self.scene.width / 2)
        self.pos = self.scene.center
        self.pos -= Point(self.radius, self.radius)

        self.transfusion_background = TransfusionBackground(scene, controller, self.pos,
                        (RGB(120, 0, 0, 120), RGB(0, 120, 0, 120), RGB(0, 0, 120, 120)))

    def process_logic(self):
        self.transfusion_background.process_logic()
        self.img = radial(self.radius, self.transfusion_background.this_color.tuple,
                          self.final_color.tuple)

    def process_draw(self):
        self.scene.screen.blit(self.img, (self.pos.x, self.pos.y))