from drawable_objects.usable_object import UsableObject
from geometry.point import Point

from scenes.base import Scene
from controller.controller import Controller


class Ladder(UsableObject):
    """
        Класс лестницы, с которой игрок может взаимодействовать,
        при взаимодействии отправляет игрока на сцену SCENE_INDEX
        """
    IMAGE_ZOOM = 0.8

    def __init__(self, scene: Scene, controller: Controller, pos: Point, angle: float = 0):
        super().__init__(scene, controller, 'level_objects.ladder',
                         pos, angle, Ladder.IMAGE_ZOOM)

    def activate(self):
        self.scene.game.set_scene_with_index(self.scene.game.SPACESHIP_SCENE_INDEX)
