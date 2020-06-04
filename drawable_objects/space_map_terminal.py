from controller.controller import Controller
from drawable_objects.usable_object import UsableObject
from geometry.point import Point
from scenes.base import Scene
from utils.sound import SoundManager


class SpaceMapTerminal(UsableObject):
    IMAGE_ZOOM = 0.8
    ACTIVATE_SOUND = 'usable.terminal'

    def __init__(self, scene: Scene, controller: Controller, pos: Point, angle: float = 0):
        super().__init__(scene, controller, 'level_objects.terminal_up',
                         pos, angle, SpaceMapTerminal.IMAGE_ZOOM)

    def activate(self):
        SoundManager.play_sound(SpaceMapTerminal.ACTIVATE_SOUND)
        from scenes.game.spacemap import SpacemapScene
        spacemap_scene = SpacemapScene(self.scene.game)
        self.scene.game.set_scene(spacemap_scene)
