from typing import List
from random import random

from constants.planets_generation import ESTIMATED_SPACE_SIZE
from geometry.point import Point
from geometry.distances import dist
from drawable_objects.planet import Planet
from scenes.base import Scene
from controller.controller import Controller


class HillFunction:
    """
    Функция "горки" от одного аргумента. Здесь реализована в виде отраженной относительно Ox и смещенной
    функции модуля.

    :param center: абсцисса вершины "горки"
    :param range: длинна горки в каждом из двух направлений
    :param height: высота "горки"
    """
    def __init__(self, center: float, range: float, height: float=1):
        self.__center = center
        self.__range = range
        self.__height = height

    def value(self, x: float) -> float:
        if abs(x - self.__center) > self.__range:
            return 0
        return self.__height - abs(x - self.__center) * self.__height / self.__range


class FeaturesArranger:
    """
    Расстановщик характеристик планет. На основе уже сгенерированных центров планет генерирует сами объекты
    планет. Назначает планетам биомы вероятностно, но по определенным правилам: чем больше абсцисса центра,
    тем сложнее в среднем биом для прохождения. Относительная вероятность появления биома задается соответствующей
    функцией из PROBABILITY_FUNC. Также первой в списке планет идет стартовая. У стартовой планеты всегда самый
    легкий биом.
    """

    PROBABILITY_FUNC = [
        HillFunction(0, 250, 1.5),
        HillFunction(250, 250),
        HillFunction(500, 250, 0.75),
        HillFunction(750, 250),
        HillFunction(1000, 250, 1.5),
    ]
    START_POSITION = Point(0, ESTIMATED_SPACE_SIZE[1] / 2)

    def __init__(self, controller: Controller, spacemap_scene: Scene):
        self.__controller = controller
        self.__spacemap_scene = spacemap_scene

    def __start_planet_to_front(self, planets_centers: List[Point]):
        """
        Перемещение центра стартовой планеты в начало списка. Стартовой выбирается ближайшая к START_POSITION
        планета.
        """
        for i in range(1, len(planets_centers)):
            if dist(planets_centers[0], self.START_POSITION) > dist(planets_centers[i], self.START_POSITION):
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
                self.__get_random_value(planets_centers[i].x) if i > 0 else 0,
            ))
        return planets

    def __transform_values(self, values: List[float]):
        """
        Преобразование значений функций относительной вероятности для последующего получения результата по случайному
        вещественному числу: нормирование и замена самих значений на их префиксные суммы.
        """
        values_sum = sum(values)
        for i in range(len(values)):
            values[i] /= values_sum
        for i in range(1, len(values)):
            values[i] += values[i - 1]

    def __get_random_value(self, x: float):
        """
        Получение случайного значения от 0 до размера PROBABILITY_FUNC - 1 включительно. Генерируется случайное
        вещественное число от 0 до 1 и по нему определяется результат. Вероятность каждого результата
        пропорциональна значению соответствующей функции.

        :param x: аргумент функциям относительной вероятности
        """
        values = [function.value(x) for function in self.PROBABILITY_FUNC]
        self.__transform_values(values)
        random_number = random()
        for i in range(len(values) - 1):
            if random_number < values[i]:
                return i
        return len(values) - 1
