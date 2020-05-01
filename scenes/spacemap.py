from drawable_objects.button import Button
from drawable_objects.planet import Planet
from geometry.point import Point
from scenes.base import Scene


class SpacemapScene(Scene):
    """
    Сцена звездной карты

    :param game: игра, создающая сцену
    """

    def __init__(self, game):
        super().__init__(game)
