import pygame

from math import pi

from drawable_objects.bed import Bed
from scenes.game.level import LevelScene
from geometry.point import Point, tuple_to_point
from map.spaceship_grid import SpaceshipGrid
from drawable_objects.space_map_terminal import SpaceMapTerminal
from drawable_objects.clone_capsule import CloneCapsule
from drawable_objects.weapon_shelf import WeaponShelf
from drawable_objects.analyser import WeaponAnalyser
from drawable_objects.base import SurfaceObject
from drawable_objects.player import Player
from space.common_game_data import CommonGameData
from utils.timer import Timer
from utils.image import ImageManager


class SpaceshipScene(LevelScene):
    """
    Класс сцены космического корабля.

    :param game: игра, создающая сцену
    """

    TOP_LEFT_CORNER_BIAS = 45
    CELL_SIZE = 25
    ROOM_WIDTH = 25
    ROOM_HEIGHT = 13
    PLAYER_SPAWN_POINT = Point(1, 1) * TOP_LEFT_CORNER_BIAS * \
        CELL_SIZE + Point(ROOM_WIDTH, ROOM_HEIGHT) * CELL_SIZE / 2
    DATA_FILENAME = 'spaceship'
    CONGRATULATION_DELAY = 20
    DRAW_GRID = False

    def __init__(self, game):
        super().__init__(game, self.DATA_FILENAME)
        self.grid = SpaceshipGrid(self, self.game.controller, Point(0, 0),
                                  self.ROOM_WIDTH, self.ROOM_HEIGHT, self.TOP_LEFT_CORNER_BIAS)
        self.congratulation_timer = Timer(self.CONGRATULATION_DELAY)
        self.create_background()

    def create_background(self):
        size = (ImageManager.get_height('other.spaceship', 1), ImageManager.get_width('other.spaceship', 1))
        surface = pygame.Surface(size)
        ImageManager.process_draw('other.spaceship', tuple_to_point(size) / 2, surface, 1, pi / 2)
        background_image_pos = Point(self.ROOM_WIDTH, self.ROOM_HEIGHT) * self.CELL_SIZE / 2
        background_image_pos += Point(1, 1) * self.TOP_LEFT_CORNER_BIAS * self.CELL_SIZE
        background_image_pos += Point(20, 5)
        self.background = SurfaceObject(surface, self, self.game.controller, background_image_pos)

    def initialize(self):
        """
        Инициализация для космического корабля означает создание игрока и общих данных игры (так это первая
        сцена, появляющаяся в новом игровом мире), а также объектов на корабле.
        """
        self.player = Player(self, self.game.controller,
                             self.PLAYER_SPAWN_POINT)
        self.common_data = CommonGameData(self)
        self.common_data.initialize()

        bed_spawn_point = Point(3, 3)
        bed_spawn_point += Point(1, 1) * self.TOP_LEFT_CORNER_BIAS
        bed_spawn_point *= self.CELL_SIZE

        capsule_spawn_point = Point(self.ROOM_WIDTH - 3, self.ROOM_HEIGHT - 3)
        capsule_spawn_point += Point(1, 1) * self.TOP_LEFT_CORNER_BIAS
        capsule_spawn_point *= self.CELL_SIZE
        terminal_spawn_point = Point(self.ROOM_WIDTH / 2, 1.3)
        terminal_spawn_point += Point(1, 1) * self.TOP_LEFT_CORNER_BIAS
        terminal_spawn_point *= self.CELL_SIZE
        analyser_spawn_point = Point((self.ROOM_WIDTH * 0.80), 1.5)
        analyser_spawn_point += Point(1, 1) * self.TOP_LEFT_CORNER_BIAS
        analyser_spawn_point *= self.CELL_SIZE

        shelf1_spawn_point = Point(3, self.ROOM_HEIGHT - 1)
        shelf1_spawn_point += Point(1, 1) * self.TOP_LEFT_CORNER_BIAS
        shelf1_spawn_point *= self.CELL_SIZE
        shelf2_spawn_point = Point(8, self.ROOM_HEIGHT - 1)
        shelf2_spawn_point += Point(1, 1) * self.TOP_LEFT_CORNER_BIAS
        shelf2_spawn_point *= self.CELL_SIZE

        self.game_objects.append(
            Bed(self, self.game.controller, bed_spawn_point))
        self.game_objects.append(SpaceMapTerminal(
            self, self.game.controller, terminal_spawn_point, 0))
        self.game_objects.append(CloneCapsule(
            self, self.game.controller, capsule_spawn_point, pi / 2))
        self.game_objects.append(WeaponAnalyser(
            self, self.game.controller, analyser_spawn_point, 0))
        self.game_objects.append(WeaponShelf(
            self, self.game.controller, shelf1_spawn_point, 0, 'Pistol'))
        self.game_objects.append(WeaponShelf(
            self, self.game.controller, shelf2_spawn_point, 0, 'TwoBarrelShotgun'))

    def load_common_data(self):
        super().load_common_data()
        if self.common_data.is_space_completed() and not self.common_data.user_congratulated:
            self.congratulation_timer.start()

    def process_all_logic(self):
        super().process_all_logic()
        self.congratulation_timer.process_logic()
        if self.congratulation_timer.is_alarm:
            self.common_data.user_congratulated = True
            self.game.set_scene_with_index(self.game.VICTORY_SCENE_INDEX)

    def game_draw(self):
        self.background.process_draw()
        super().game_draw()
