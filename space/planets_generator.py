from typing import List

from controller.controller import Controller
from scenes.base import Scene
from space.centers_arranger import CentersArranger
from space.features_arranger import FeaturesArranger
from drawable_objects.planet import Planet


class PlanetsGenerator:
    """
    Генератор планет на космической карте. Собирает воедино функционал CentersArranger'а и FeaturesArranger'a.
    """

    PLANETS_NUMBER = 20

    def __init__(self, controller: Controller, spacemap_scene: Scene):
        self.__centers_arranger = CentersArranger(self.PLANETS_NUMBER)
        self.__features_arranger = FeaturesArranger(controller, spacemap_scene)

    def generate(self) -> List[Planet]:
        planets_centers = self.__centers_arranger.generate()
        planets = self.__features_arranger.generate(planets_centers)
        return planets
