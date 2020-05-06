from drawable_objects.base import UsableObject
from geometry.point import Point

from scenes.base import Scene
from controller.controller import Controller

from drawable_objects.player import Player


class SpaceMapTerminal(UsableObject):

    IMAGE_ZOOM = 0.8

    def __init__(self, scene: Scene, controller: Controller, pos: Point, angle: float = 0):
        super().__init__(scene, controller, 'level_objects.terminal_up',
                         pos, angle, SpaceMapTerminal.IMAGE_ZOOM)

    def activate(self):
        self.scene.game.toggle_scene(self.scene.game.SPACEMAP_SCENE_INDEX)
