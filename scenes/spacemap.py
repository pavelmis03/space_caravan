from scenes.base import ConservableScene
from space.planets_generator import PlanetsGenerator
from geometry.rectangle import Rectangle


class SpacemapScene(ConservableScene):
    """
    Сцена звездной карты

    :param game: игра, создающая сцену
    """
    DATA_FILENAME = 'spacemap.txt'

    def __init__(self, game):
        super().__init__(game, self.DATA_FILENAME)

    def initialize(self):
        space_rectangle = Rectangle(0, 0, self.game.width, self.game.height)
        planets_generator = PlanetsGenerator(space_rectangle, 12, self.game.controller, self)
        self.interface_objects = planets_generator.generate()
