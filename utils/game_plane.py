from math import floor

from geometry.point import Point, point_to_tuple
from drawable_objects.base import GameSprite


class GamePlane:
    CHUNK_SIZE = 100

    def __init__(self):
        self.objects = {}

    def get_chunk(self, pos: Point) -> Point:
        chunk = Point(floor(pos.x / GamePlane.CHUNK_SIZE), floor(pos.y / GamePlane.CHUNK_SIZE))
        return chunk

    def insert(self, game_object: GameSprite, pos: Point):
        chunk_tuple = point_to_tuple(self.get_chunk(pos))
        if chunk_tuple not in self.objects:
            self.objects[chunk_tuple] = set()
        self.objects[chunk_tuple].add(game_object)

    def erase(self, game_object: GameSprite, pos: Point):
        chunk_tuple = point_to_tuple(self.get_chunk(pos))
        self.objects[chunk_tuple].remove(game_object)
        if len(self.objects[chunk_tuple]) == 0:
            self.objects.pop(chunk_tuple)

    def do_step(self, game_object: GameSprite, pos: Point, new_pos: Point):
        old_chunk = self.get_chunk(pos)
        new_chunk = self.get_chunk(new_pos)
        if old_chunk != new_chunk:
            self.erase(game_object, pos)
            self.insert(game_object, new_pos)
            print("New chunk is {}, {}".format(new_chunk.x, new_chunk.y))

    def get_neighbours(self, pos: Point):
        chunk = self.get_chunk(pos)
        neighbours = []
        for delta_x in range(-1, 2):
            for delta_y in range(-1, 2):
                chunk_tuple = point_to_tuple(chunk + Point(delta_x + delta_y))
                if chunk_tuple in self.objects:
                    for item in self.objects[chunk_tuple]:
                        neighbours.append(item)
        return neighbours
