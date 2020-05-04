from console.console import Console
from console.entry import Entry
from drawable_objects.CloneCapsule import CloneCapsule
from drawable_objects.interface.pause_manager import PauseManager
from drawable_objects.player import Player
from scenes.base import GameScene
from geometry.point import Point
from map.spaceship_grid import SpaceshipGrid
from utils.game_plane import GamePlane
from utils.image import ImageManager

from drawable_objects.space_map_terminal import SpaceMapTerminal


class SpaceshipScene(GameScene):
    def __init__(self, game):
        super().__init__(game)

        top_left_cornor_bias = 25  # Смещение грида от угла для однообразного управления
        bias_point = Point(top_left_cornor_bias, top_left_cornor_bias) * 25 # Левый верхний угол корабля
        room_width = 30
        room_height = 20
        tile_size = 25  # Размер клетки в ширину и длину, заменить на константу, когда появится
        player_spawn_point = bias_point + Point(room_width / 2, room_height / 2) * tile_size

        # Терминал спавнится относительно размера его картинки на нижней стороне корабля в середине
        terminal_spawn_point = bias_point + Point((room_width / 2) * tile_size, room_height * tile_size -
            ImageManager.get_height('level_objects.terminal_up', SpaceMapTerminal.IMAGE_ZOOM) / 2)

        """clonecapsule_spawn_point = player_spawn_point + \
                               Point((room_width / 2 - 2) * 25, (room_height - 3) * 25)"""

        self.plane = GamePlane()
        self.player = Player(self, self.game.controller, player_spawn_point, 0)
        self.game.controller.input_objects.append(self.player)
        self.grid = SpaceshipGrid(self, self.game.controller, Point(
            0, 0), 25, 25, room_width, room_height, top_left_cornor_bias)

        self.game_objects.append(SpaceMapTerminal(
            self, self.game.controller, terminal_spawn_point, 0))
        """self.game_objects.append(CloneCapsule(
            self, self.game.controller, clonecapsule_spawn_point, 0))"""

        self.pause_manager = PauseManager(self, self.game.controller)
        self.interface_objects.append(self.pause_manager)
        self.game.controller.input_objects.append(self.pause_manager)
