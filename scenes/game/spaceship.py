from typing import Dict

from scenes.game.base import GameScene
from geometry.point import Point
from map.spaceship_grid import SpaceshipGrid
from drawable_objects.space_map_terminal import SpaceMapTerminal
from drawable_objects.player import Player


class SpaceshipScene(GameScene):
    """
    Класс сцены космического корабля.

    :param game: игра, создающая сцену
    """

    TOP_LEFT_CORNER_BIAS = 25
    CELL_SIZE = 25
    ROOM_WIDTH = 30
    ROOM_HEIGHT = 20
    PLAYER_SPAWN_POINT = Point(1, 1) * TOP_LEFT_CORNER_BIAS * CELL_SIZE + Point(2, 2) * CELL_SIZE
    DATA_FILENAME = 'spaceship'

    def __init__(self, game):
        super().__init__(game, self.DATA_FILENAME)

    def initialize(self):
        """
        Инициализация для космического корабля означает создание игрока (так это первая сцена, появляющаяся в
        новом игровом мире), а также объектов на корабле.
        """
        self.grid = SpaceshipGrid(self, self.game.controller, Point(0, 0), self.CELL_SIZE, self.CELL_SIZE,
                                  self.ROOM_WIDTH, self.ROOM_HEIGHT, self.TOP_LEFT_CORNER_BIAS)
        terminal_spawn_point = Point((self.ROOM_WIDTH / 2) * self.CELL_SIZE, (self.ROOM_HEIGHT - 2) * self.CELL_SIZE)
        terminal_spawn_point += Point(1, 1) * self.TOP_LEFT_CORNER_BIAS * self.CELL_SIZE
        self.game_objects.append(SpaceMapTerminal(
            self, self.game.controller, terminal_spawn_point, 0))
        self.player = Player(self, self.game.controller, self.PLAYER_SPAWN_POINT)
        self.game.controller.input_objects.append(self.player)

    def from_dict(self, data_dict: Dict):
        super().from_dict(data_dict)
        self.grid = SpaceshipGrid(self, self.game.controller, Point(0, 0), 25, 25,
                                  self.ROOM_WIDTH, self.ROOM_HEIGHT, self.TOP_LEFT_CORNER_BIAS)

    def to_dict(self) -> Dict:
        return super().to_dict()
