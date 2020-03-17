from drawable_objects.background.rgb import RGB
from utils.image import ImageManager
from drawable_objects.base import SpriteObject
from geometry.point import Point
from controller.controller import Controller
from scenes.base import Scene
from PIL import Image
from math import sqrt

class GradientBackground(SpriteObject):
    def __init__(self, scene: Scene, controller: Controller,
                 image_name: str, pos: Point,
                 start_color: RGB, final_color: RGB,
                 angle: float = 0, zoom: float = 1):
        pos = Point(scene.game.width / 2, scene.game.height / 2)
        super().__init__(scene, controller, image_name, pos, angle, zoom)
        self.start_color = start_color
        self.final_color = final_color

        imgsize = (self.scene.game.width, self.scene.game.height)  # The size of the image

        image = Image.new('RGB', imgsize)  # Create the image

        innerColor = self.start_color.tuple  # Color at the center
        outerColor = self.final_color.tuple # Color at the corners
        print('begin')
        for y in range(imgsize[1]):
            for x in range(imgsize[0]):
                # Find the distance to the center
                distanceToCenter = sqrt((x - imgsize[0] / 2) ** 2 + (y - imgsize[1] / 2) ** 2)

                # Make it on a scale from 0 to 1
                distanceToCenter = float(distanceToCenter) / (sqrt(2) * imgsize[0] / 2)

                # Calculate r, g, and b values
                r = outerColor[0] * distanceToCenter + innerColor[0] * (1 - distanceToCenter)
                g = outerColor[1] * distanceToCenter + innerColor[1] * (1 - distanceToCenter)
                b = outerColor[2] * distanceToCenter + innerColor[2] * (1 - distanceToCenter)

                # Place the pixel
                image.putpixel((x, y), (int(r), int(g), int(b)))

        image.save(ImageManager.img_name_to_path(self.image_name))
        ImageManager.load_img(self.image_name)
        print('end')