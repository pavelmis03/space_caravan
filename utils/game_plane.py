from math import floor
from typing import Tuple, List, ClassVar

from geometry.point import Point
from drawable_objects.base import GameSprite


class GamePlane:
    """
    Класс игровой плоскости. Неявно разбивает плоскость на квадраты (чанки) заданного размера. Нужен для оптимизации
    обработки коллизий.
    """

    CHUNK_SIZE = 100

    def __init__(self):
        self.__objects = {}

    def get_chunk(self, pos: Point) -> Tuple[int, int]:
        """
        Получение координат чанка по координатам точки на плоскости. Чанк характеризуется двумя индексами, как
        элемент двумерного массива (но на деле используется не массив, а словарь).

        :param pos: точка на плоскости
        :return: координаты соответствующего чанка
        """
        chunk = int(floor(pos.x / GamePlane.CHUNK_SIZE)), int(floor(pos.y / GamePlane.CHUNK_SIZE))
        return chunk

    def insert(self, game_object: GameSprite, pos: Point):
        """
        Добавление ссылки на игровой объект в структуру данных по точке.

        :param game_object: игровой объект
        :param pos: точка на плоскости
        """
        chunk = self.get_chunk(pos)
        if chunk not in self.__objects:
            self.__objects[chunk] = set()
        self.__objects[chunk].add(game_object)

    def erase(self, game_object: GameSprite, pos: Point):
        """
        Удаление ссылки на игровой объект из структуры данных по точке.

        :param game_object: игровой объект
        :param pos: точка на плоскости
        """
        chunk = self.get_chunk(pos)
        self.__objects[chunk].remove(game_object)
        if len(self.__objects[chunk]) == 0:
            self.__objects.pop(chunk)

    def do_step(self, game_object: GameSprite, pos: Point, new_pos: Point):
        """
        Фиксирование перемещения объекта. Должно вызываться объектами. Если чанк меняется, ссылка на объект
        перемещается в структуре данных.

        :param game_object: игровой объект
        :param pos: старое положение объекта
        :param new_pos: новое положение объекта
        """
        old_chunk = self.get_chunk(pos)
        new_chunk = self.get_chunk(new_pos)
        if old_chunk != new_chunk:
            self.erase(game_object, pos)
            self.insert(game_object, new_pos)

    def get_objects_from_chunk(self, chunk: Tuple[int, int], objects_class: type) -> List[type]:
        """
        Получение объектов в заданном чанке по классу.
        """
        if chunk not in self.__objects:
            return list()
        objects_from_chunk = list()
        for item in self.__objects[chunk]:
            if isinstance(item, objects_class):
                objects_from_chunk.append(item)
        return objects_from_chunk

    def get_neighbours(self, pos: Point, neighbours_class: type) -> List[type]:
        """
        Получение списка ссылок на объекты определенного класса поблизости -
        в чанке точки и восьми соседних.

        Внимание! При запросе по центру некоторого игрового объекта в списке ближайших
        его же класса будет в том числе сам объект!

        :param pos: точка на плоскости
        :param neighbours_class: класс
        :return: список объектов в ближайших чанках
        """
        chunk = self.get_chunk(pos)
        neighbours = []
        for delta_x in range(-1, 2):
            for delta_y in range(-1, 2):
                neighbour_chunk = (chunk[0] + delta_x, chunk[1] + delta_y)
                objects_from_chunk = self.get_objects_from_chunk(neighbour_chunk, neighbours_class)
                for item in objects_from_chunk:
                    neighbours.append(item)
        return neighbours
