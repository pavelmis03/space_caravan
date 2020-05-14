from geometry.point import Point
from drawable_objects.player import Player
from map.grid import Grid

class Camera:
    MOUSE_SHIFT_SENSIVITY = 1 / 16
    def __init__(self, game, grid: Grid, player: Player):
        self.__game = game
        self.__grid = grid
        self.__player = player

    def get_relative_center(self) -> Point:
        result = self.__player.pos - self.__game.screen_rectangle.center

        result += self.__camera_transition_by_mouse

        result = self.__grid.get_correct_relative_pos(result)

        return result

    @property
    def __camera_transition_by_mouse(self) -> Point:
        mouse_pos = self.__game.controller.get_mouse_pos()
        mouse_transition = mouse_pos - Point(self.__game.width / 2, self.__game.height / 2)
        return mouse_transition * Camera.MOUSE_SHIFT_SENSIVITY

