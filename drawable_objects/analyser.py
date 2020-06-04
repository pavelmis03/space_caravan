from controller.controller import Controller
from drawable_objects.interface.message_display import MessageDisplay
from drawable_objects.usable_object import UsableObject
from geometry.point import Point
from scenes.base import Scene
from utils.sound import SoundManager


class WeaponAnalyser(UsableObject):
    IMAGE_ZOOM = 0.05
    ACTIVATE_SOUND = 'usable.terminal'

    def __init__(self, scene: Scene, controller: Controller, pos: Point, angle: float = 0):
        super().__init__(scene, controller, 'level_objects.analisor',
                         pos, angle, WeaponAnalyser.IMAGE_ZOOM)
        self.message = MessageDisplay(self.scene, self.scene.game.controller, self.scene.player.weapon.DESCRIPTION)

    def activate(self):
        SoundManager.play_sound(WeaponAnalyser.ACTIVATE_SOUND)
        self.message.buttons.widgets[0].set_text(self.scene.player.weapon.DESCRIPTION)
        self.message.show()
