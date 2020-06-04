from controller.controller import Controller
from drawable_objects.usable_object import UsableObject
from geometry.point import Point
from utils.sound import SoundManager


class Bed(UsableObject):
    """
    Класс кровати для уровня корабля.
    Необходим для выхода из корабля в главное меню
    """
    IMAGE_ZOOM = 0.8
    ACTIVATION_SOUND = 'usable.ladder'

    def __init__(self, scene, controller: Controller, pos: Point, angle: float = 0):
        super().__init__(scene, controller, 'level_objects.bed',
                         pos, angle, Bed.IMAGE_ZOOM)

    def activate(self):
        """
        Действия при активации. Именно здесь создается сцена корабля, так работает загрузка сцен.
        """
        SoundManager.play_sound(Bed.ACTIVATION_SOUND)
        self.scene.game.set_scene_with_index(self.scene.game.MAIN_MENU_SCENE_INDEX)