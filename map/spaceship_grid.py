from map.collision_grid import CollisionGrid
from geometry.point import Point
from scenes.base import Scene

class SpaceshipGrid(CollisionGrid):
    """
    Сетка космического корабля.
    """
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
