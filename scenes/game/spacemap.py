from scenes.game.base import GameScene
from space.planets_generator import PlanetsGenerator


class SpacemapScene(GameScene):
    """
    Сцена звездной карты.

    :param game: игра, создающая сцену
    """
    DATA_FILENAME = 'spacemap'

    def __init__(self, game):
        super().__init__(game, self.DATA_FILENAME)

    def initialize(self):
        """
        Для звездной карты инициализация означает создание планет, чем занимается PlanetsGenerator.
        """
        planets_generator = PlanetsGenerator(self.game.controller, self)
        self.interface_objects = planets_generator.generate()
