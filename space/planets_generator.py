from random import random, choice
from typing import List

from geometry.point import Point
from geometry.rectangle import Rectangle
from geometry.vector import sign, length, normalized
from geometry.distances import dist
from scenes.base import Scene
from drawable_objects.planet import Planet
from controller.controller import Controller


class PlanetsGenerator:
    def __init__(self, space_rectangle: Rectangle, planets_number: int,
                 controller: Controller, spacemap_scene: Scene):
        self.__space_rectangle = space_rectangle
        self.__planets_number = planets_number
        self.__spacemap_scene = spacemap_scene
        self.__controller = controller

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
        planets_centers = list()
        for i in range(self.__planets_number):
            while True:
                current_center = self.__get_random_point_inside(self.__space_rectangle)
                if not self.__already_in_list(planets_centers, current_center):
                    break
            planets_centers.append(current_center)
        return planets_centers

    def __push_till_dist(self, planets_centers: List[Point], distance: int, delta: int) -> bool:
        flag = True
        velocity = [Point() for _ in range(len(planets_centers))]
        for k in range(len(planets_centers) * len(planets_centers)):
            for i in range(len(planets_centers)):
                velocity[i] = Point(0, 0)
            for i in range(len(planets_centers)):
                if planets_centers[i].x < self.__space_rectangle.left + distance:
                    velocity[i].x += delta
                if planets_centers[i].x > self.__space_rectangle.right - distance:
                    velocity[i].x += -delta
                if planets_centers[i].y < self.__space_rectangle.top + distance:
                    velocity[i].y += delta
                if planets_centers[i].y > self.__space_rectangle.bottom - distance:
                    velocity[i].y += -delta
                for j in range(len(planets_centers)):
                    if i != j:
                        v = planets_centers[i] - planets_centers[j]
                        if length(v) < 2 * distance:
                            velocity[i] += normalized(v) * delta
            for i in range(len(planets_centers)):
                planets_centers[i] += velocity[i]

            flag = False
            for i in range(len(planets_centers)):
                if sign(length(velocity[i])) != 0:
                    flag = True
            if not flag:
                break

        return not flag

    def __spread_centers(self, planets_centers: List[Point]):
        distance = 0
        delta = 5
        while self.__push_till_dist(planets_centers, distance, delta):
            distance += delta

    def __arrange_planets_centers(self) -> List[Point]:
        planets_centers = self.__generate_random_centers()
        self.__spread_centers(planets_centers)
        return planets_centers

    def __generate_planets_with_centers(self, planets_centers: List[Point]) -> List[Planet]:
        planets = list()
        for center in planets_centers:
            planets.append(Planet(
                self.__spacemap_scene,
                self.__controller,
                center,
                choice(Planet.BIOMS)
            ))
        return planets

    def generate(self) -> List[Planet]:
        planets_centers = self.__arrange_planets_centers()
        planets = self.__generate_planets_with_centers(planets_centers)
        return planets

