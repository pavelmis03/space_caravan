from math import floor

from geometry.point import Point, point_to_tuple
from drawable_objects.base import GameSprite


class GamePlane:
    """
    Класс игровой плоскости. Неявно разбивает плоскость на квадраты (чанки) заданного размера. Нужен для оптимизации
    обработки коллизий.
    """

    CHUNK_SIZE = 100

    def __init__(self):
        self.objects = {}

    def get_chunk(self, pos: Point) -> Point:
        """
        Получение координат чанка по координатам точки на плоскости.

        :param pos: точка на плоскости
        :return: координаты соответствующего чанка
        """
        chunk = Point(floor(pos.x / GamePlane.CHUNK_SIZE),
                      floor(pos.y / GamePlane.CHUNK_SIZE))
        return chunk

    def insert(self, game_object: GameSprite, pos: Point):
        """
        Добавление ссылки на игровой объект в структуру данных по точке.

        :param game_object: игровой объект
        :param pos: точка на плоскости
        """
        chunk_tuple = point_to_tuple(self.get_chunk(pos))
        if chunk_tuple not in self.objects:
            self.objects[chunk_tuple] = set()
        self.objects[chunk_tuple].add(game_object)

    def erase(self, game_object: GameSprite, pos: Point):
        """
        Удаление ссылки на игровой объект из структуры данных по точке.

        :param game_object: игровой объект
        :param pos: точка на плоскости
        """
        chunk_tuple = point_to_tuple(self.get_chunk(pos))
        self.objects[chunk_tuple].remove(game_object)
        if len(self.objects[chunk_tuple]) == 0:
            self.objects.pop(chunk_tuple)

    def do_step(self, game_object: GameSprite, pos: Point, new_pos: Point):
        """
        Фиксирование перемещение объекта. Вызывается игровыми объектами при перемещении. Если чанк меняется, ссылка
        на объект перемещается в структуре данных.

        :param game_object: игровой объект
        :param pos: старое положение объекта
        :param new_pos: новое положение объекта
        """
        old_chunk = self.get_chunk(pos)
        new_chunk = self.get_chunk(new_pos)
        if old_chunk != new_chunk:
            self.erase(game_object, pos)
            self.insert(game_object, new_pos)
            #print("New chunk is {}, {}".format(new_chunk.x, new_chunk.y))

    def get_neighbours(self, pos: Point):
        """
        Получение списка ссылок на ближайшие объекты.

        Внимание! При запросе по центру некоторого игрового объекта в списке ближайших будет и сам объект!

        :param pos: точка на плоскости
        :return: список объектов в ближайших чанках
        """
        chunk = self.get_chunk(pos)
        neighbours = []
        for delta_x in range(-1, 2):
            for delta_y in range(-1, 2):
                chunk_tuple = point_to_tuple(chunk + Point(delta_x + delta_y))
                if chunk_tuple in self.objects:
                    for item in self.objects[chunk_tuple]:
                        neighbours.append(item)
        return neighbours
