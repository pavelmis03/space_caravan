from drawable_objects.button import Button
from drawable_objects.planet import Planet
from geometry.point import Point
from scenes.base import Scene


class SpacemapScene(Scene):
    """
    Сцена звездной карты


    :param game: игра, создающая сцену Bullet(self.scene, self.controller, self.pos, self.angle)
    """
    def __init__(self, game):
        super().__init__(game)
        self.interface_objects.append(Planet(self, self.game.controller, 'planet', Point(200, 200), 0, 0.09,
                                             self.game.set_scene, {'scene_index': self.game.MAIN_SCENE_INDEX}))
        self.interface_objects.append(Planet(self, self.game.controller, 'planet', Point(600, 600), 0, 0.09,
                                             self.game.set_scene, {'scene_index': self.game.MAIN_SCENE_INDEX}))


