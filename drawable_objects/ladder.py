from drawable_objects.usable_object import UsableObject
from geometry.point import Point

from scenes.base import Scene
from controller.controller import Controller

class Ladder(UsableObject):
    """
    Класс уводящей с уровня лестницы, с которой игрок может взаимодействовать. При взаимодействии устанавливается
    сцена корябля.
    """
    IMAGE_ZOOM = 0.8

    def __init__(self, scene: Scene, controller: Controller, pos: Point = Point(), angle: float = 0):
        super().__init__(scene, controller, 'level_objects.ladder',
                         pos, angle, Ladder.IMAGE_ZOOM)

    def activate(self):
        """
        Действия при активации. Именно здесь создается сцена корабля, так работает загрузка сцен.
        """
        from scenes.game.spaceship import SpaceshipScene  # В обход циклических import'ов
        spaceship_scene = SpaceshipScene(self.scene.game)
        spaceship_scene.load()
        self.scene.game.set_scene(spaceship_scene)
