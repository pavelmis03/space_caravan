from controller.controller import Controller
from drawable_objects.usable_object import UsableObject
from geometry.point import Point
from scenes.base import Scene
from scenes.spacemap import SpacemapScene


class SpaceMapTerminal(UsableObject):
    IMAGE_ZOOM = 0.8

    def __init__(self, scene: Scene, controller: Controller, pos: Point, angle: float = 0):
        super().__init__(scene, controller, 'level_objects.terminal_up',
                         pos, angle, SpaceMapTerminal.IMAGE_ZOOM)
        self.spacemap_scene = SpacemapScene(self.scene.game)
        self.spacemap_generated = False

    def activate(self):
        if not self.spacemap_generated:
            self.spacemap_scene.initialize()
        else:
            self.spacemap_scene.load()
        self.scene.game.set_scene(self.spacemap_scene)
