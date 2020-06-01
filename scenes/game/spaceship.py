from scenes.game.level import LevelScene
from geometry.point import Point
from map.spaceship_grid import SpaceshipGrid
from drawable_objects.space_map_terminal import SpaceMapTerminal
from drawable_objects.clone_capsule import CloneCapsule
from drawable_objects.weapon_shelf import WeaponShelf
from drawable_objects.player import Player
from space.common_game_data import CommonGameData


class SpaceshipScene(LevelScene):
    """
    Класс сцены космического корабля.

    :param game: игра, создающая сцену
    """

    TOP_LEFT_CORNER_BIAS = 45
    CELL_SIZE = 25
    ROOM_WIDTH = 20
    ROOM_HEIGHT = 15
    PLAYER_SPAWN_POINT = Point(1, 1) * TOP_LEFT_CORNER_BIAS * \
        CELL_SIZE + Point(ROOM_WIDTH, ROOM_HEIGHT) * CELL_SIZE / 2
    DATA_FILENAME = 'spaceship'

    def __init__(self, game):
        super().__init__(game, self.DATA_FILENAME)
        self.grid = SpaceshipGrid(self, self.game.controller, Point(0, 0),
                                  self.ROOM_WIDTH, self.ROOM_HEIGHT, self.TOP_LEFT_CORNER_BIAS)

    def initialize(self):
        """
        Инициализация для космического корабля означает создание игрока и общих данных игры (так это первая
        сцена, появляющаяся в новом игровом мире), а также объектов на корабле.
        """
        capsule_spawn_point = Point(
            (self.ROOM_WIDTH / 2) * self.CELL_SIZE, (self.ROOM_HEIGHT + 2) * self.CELL_SIZE)
        capsule_spawn_point += Point(1, 1) * \
            self.TOP_LEFT_CORNER_BIAS * self.CELL_SIZE
        terminal_spawn_point = Point(
            (self.ROOM_WIDTH / 2) * self.CELL_SIZE, -1 * self.CELL_SIZE)
        terminal_spawn_point += Point(1, 1) * \
                                self.TOP_LEFT_CORNER_BIAS * self.CELL_SIZE
        shelf_spawn_point = Point(
            3 * self.CELL_SIZE, self.ROOM_HEIGHT * self.CELL_SIZE - 10)
        shelf_spawn_point += Point(1, 1) * \
                                self.TOP_LEFT_CORNER_BIAS * self.CELL_SIZE

        self.game_objects.append(SpaceMapTerminal(
            self, self.game.controller, terminal_spawn_point, 0))
        self.game_objects.append(CloneCapsule(
            self, self.game.controller, capsule_spawn_point, 0))
        self.game_objects.append(WeaponShelf(
            self, self.game.controller, shelf_spawn_point, 0))

        self.player = Player(self, self.game.controller,
                             self.PLAYER_SPAWN_POINT)
        self.common_data = CommonGameData(self)
        self.common_data.initialize()
