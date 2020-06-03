from drawable_objects.usable_object import UsableObject
from geometry.point import Point

from controller.controller import Controller
from utils.sound import SoundManager


class Ladder(UsableObject):
    """
    Класс уводящей с уровня лестницы, с которой игрок может взаимодействовать. При взаимодействии устанавливается
    сцена корябля.
    """
    IMAGE_ZOOM = 0.8
    ACTIVATION_SOUND = 'usable.ladder'

    def __init__(self, scene, controller: Controller, pos: Point, angle: float = 0):
        super().__init__(scene, controller, 'level_objects.ladder',
                         pos, angle, Ladder.IMAGE_ZOOM)

    def activate(self):
        """
        Действия при активации. Именно здесь создается сцена корабля, так работает загрузка сцен.
        """
        SoundManager.play_sound(Ladder.ACTIVATION_SOUND)
        from scenes.game.spaceship import SpaceshipScene  # В обход циклических import'ов
        spaceship_scene = SpaceshipScene(self.scene.game)
        self.scene.game.set_scene(spaceship_scene)
