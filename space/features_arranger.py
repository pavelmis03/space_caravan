from typing import List
from random import random

from geometry.point import Point
from geometry.vector import length
from drawable_objects.planet import Planet
from scenes.base import Scene
from controller.controller import Controller


class HillFunction:
    def __init__(self, center: float, height: float, harshness: float):
        self.__center = center
        self.__height = height
        self.__harshness = harshness

    def value(self, x: float) -> float:
        divisor = (x - self.__center) ** 2 * self.__harshness + 1
        return self.__height / divisor


class FeaturesArranger:
    PROBABILITY_FUNC = [
        HillFunction(0, 1, 0.2),
        HillFunction(500, 1, 1),
        HillFunction(600, 1, 1),
        HillFunction(700, 1, 1),
        HillFunction(1220, 1, 1),
    ]

    def __init__(self, controller: Controller, spacemap_scene: Scene):
        self.__controller = controller
        self.__spacemap_scene = spacemap_scene

    def __start_planet_to_front(self, planets_centers: List[Point]):
        for i in range(1, len(planets_centers)):
            if length(planets_centers[0]) > length(planets_centers[i]):
                planets_centers[0], planets_centers[i] = planets_centers[i], planets_centers[0]

    def generate(self, planets_centers: List[Point]) -> List[Planet]:
        """
        Формирование массива объектов планет по их центрам. Здесь задаются характеристики планет.
        """
        self.__start_planet_to_front(planets_centers)
        planets = list()
        for i in range(len(planets_centers)):
            planets.append(Planet(
                self.__spacemap_scene,
                self.__controller,
                planets_centers[i],
                self.__get_random_value(length(planets_centers[i])) if i > 0 else 0,
            ))
        return planets

    def __get_random_value(self, x: float):
        values = [function.value(x) for function in self.PROBABILITY_FUNC]
        summa = sum(values)
        for i in range(len(values)):
            values[i] /= summa
        for i in range(1, len(values)):
            values[i] += values[i - 1]
        random_number = random()
        for i in range(len(values) - 1):
            if random_number < values[i]:
                return i
        return len(values) - 1
