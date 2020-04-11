from map.collision_grid.collision_grid import CollisionGrid
from geometry.point import Point
from scenes.base import Scene
from controller.controller import Controller

class SpaceshipGrid(CollisionGrid):
    """
    Сетка космического корабля.
    """
    def __init__(self, scene: Scene, controller: Controller, pos: Point,
                 cell_width: int, cell_height: int,
                 width: int = 100, height: int = 100,
                 top_left_corner_bias: int = 24,
                 min_area: int = 100, min_w: int = 8, min_h: int = 8):
        self.room_width = width
        self.room_height = height
        self.top_left_corner_bias = top_left_corner_bias  # Смещение от угла для однообразного управления
        super ().__init__ (scene, controller, pos, cell_width, cell_height)

    def map_construction(self):
        width = self.top_left_corner_bias + self.room_width
        height = self.top_left_corner_bias + self.room_height
        for i in range(self.top_left_corner_bias, height):
            for j in range(self.top_left_corner_bias, width):
                self.arr[i][j] = 1
