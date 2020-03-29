from typing import List
from map.grid import Grid
from map.level.generator import LevelGenerator
from drawable_objects.base import GameSprite
from geometry.point import Point
from geometry.rectangle import Rectangle, create_rect_with_center
from controller.controller import Controller
from scenes.base import Scene
from map.level.grid_static_draw_manager import GridStaticDrawManager
from map.level.grid import LevelGrid

from drawable_objects.space_map_terminal import SpaceMapTerminal


class SpaceshipGrid(LevelGrid):
    def map_objects_init(self, width: int = 21, height: int = 21):
        self.grid_odjects.append(SpaceMapTerminal(self.scene, self.controller, Point(100, 100), 0))

        for object in self.grid_odjects:
            self.scene.game_objects.append(object)

    def map_construction(self, width: int = 21, height: int = 21):
        for i in range(width):
            for j in range(height):
                self.arr[i][j] = 1
        for i in range(height):
            self.arr[i][0] = 0
            self.arr[i][width - 1] = 0
        for i in range(width):
            self.arr[0][i] = 0
            self.arr[height - 1][i] = 0