from random import random
from typing import List

from constants.planets_generation import ESTIMATED_SPACE_SIZE
from geometry.point import Point
from geometry.rectangle import Rectangle
from geometry.line import Line, line_from_points
from geometry.vector import sign, normalized
from geometry.distances import dist, dist_squared, dist_point_line


class CentersArranger:
    """
    Генератор планет на карте космоса. Вначале расставляет планеты случайно, потом распределяет их по
    пространству гравитационными силами. Константами можно установить значения этих сил. Планеты
    отталкиваются друг от друга и от границ космоса. Силы отталкивания разбрасывают планеты по
    краям, поэтому для компенсации планеты притягиваются к центру.
    """

    ITERATIONS = 200
    BORDER_FORCE = 10000
    PLANET_FORCE = 40000
    SPACE_CENTER_KOEF = 1.2
    MIN_GRAVITY_DIST_SQUARE = 1000

    def __init__(self, planets_number: int):
        self.__space_rectangle = Rectangle(0, 0, ESTIMATED_SPACE_SIZE[0], ESTIMATED_SPACE_SIZE[1])
        self.__planets_number = planets_number

    def generate(self) -> List[Point]:
        planets_centers = self.__generate_random_centers()
        self.__spread_centers(planets_centers)
        return planets_centers

    def __already_in_list(self, points: List[Point], sample: Point) -> bool:
        for point in points:
            if sign(dist(sample, point)) == 0:
                return True
        return False

    def __get_random_point_inside(self, rectangle: Rectangle) -> Point:
        result = Point(random() * rectangle.width, random() * rectangle.height)
        result += rectangle.top_left
        return result

    def __generate_random_centers(self) -> List[Point]:
        """
        Случайно сгенерировать список центров планет в прямоугольнике космоса.
        """
        planets_centers = list()
        for i in range(self.__planets_number):
            while True:
                current_center = self.__get_random_point_inside(self.__space_rectangle)
                if not self.__already_in_list(planets_centers, current_center):
                    break
            planets_centers.append(current_center)
        return planets_centers

    def __border_gravity(self, planet_pos: Point, border_lines: List[Line]) -> Point:
        """
        Взаимодействие с границей космоса. Сила отталкивания обратно пропорциональна квадрату расстояния
        до границы, определяется константой.

        :return: вектор, на который меняется скорость планеты
        """
        result = Point(0, 0)
        for line in border_lines:
            direction_vector = -normalized(line.get_normal())
            dist_square = dist_point_line(planet_pos, line) ** 2
            dist_square = max(dist_square, CentersArranger.MIN_GRAVITY_DIST_SQUARE)
            result += direction_vector / dist_square * CentersArranger.BORDER_FORCE
        return result

    def __planet_gravity(self, planet_pos: Point, other_planet_pos: Point) -> Point:
        """
        Взаимодействие с другой планетой. Сила отталкивания обратно пропорциональна квадрату
        расстояния между планетами, определяется константой.

        :return: вектор, на который меняется скорость планеты
        """
        direction_vector = normalized(planet_pos - other_planet_pos)
        dist_square = dist_squared(planet_pos, other_planet_pos)
        dist_square = max(dist_square, CentersArranger.MIN_GRAVITY_DIST_SQUARE)
        return direction_vector / dist_square * CentersArranger.PLANET_FORCE

    def __space_center_gravity(self, planet_pos: Point) -> Point:
        """
        Взаимодействие с центром космоса. Сила притяжения не зависит от расстояния, определяется
        константой.

        :return: вектор, на который меняется скорость планеты
        """
        direction_vector = normalized(self.__space_rectangle.center - planet_pos)
        return direction_vector * CentersArranger.SPACE_CENTER_KOEF

    def __gravity_iteration(self, planets_centers: List[Point], border_lines: List[Line]):
        """
        Итерация гравитационных взаимодействий. Формируется массив векторов скоростей планет, затем
        планеты сдвигаются на эти векторы.
        """
        velocity = [Point() for _i in range(len(planets_centers))]
        for i in range(len(planets_centers)):
            velocity[i] += self.__border_gravity(planets_centers[i], border_lines)
            velocity[i] += self.__space_center_gravity(planets_centers[i])
            for j in range(len(planets_centers)):
                if i != j:
                    velocity[i] += self.__planet_gravity(planets_centers[i], planets_centers[j])
        for i in range(len(planets_centers)):
            planets_centers[i] += velocity[i]

    def __spread_centers(self, planets_centers: List[Point]):
        border_segments = self.__space_rectangle.get_edges()
        border_lines = [line_from_points(segment.p1, segment.p2) for segment in border_segments]
        for _i in range(CentersArranger.ITERATIONS):
            self.__gravity_iteration(planets_centers, border_lines)
