from geometry.point import Point, tuple_to_point
from geometry.rectangle import Rectangle
from drawable_objects.player import Player
from map.grid import Grid


class Camera:
    MOUSE_SHIFT_SENSIVITY = 1 / 16

    def __init__(self, game, grid: Grid, player: Player):
        self.__game = game
        self.__grid = grid
        self.__player = player
        self.__transition = CameraTransition(self.__game, self.__player)

    def get_relative_center(self) -> Point:
        result = self.__player.pos - self.__game.screen_rectangle.center

        result += self.__get_camera_shift_by_mouse()
        old = result
        result = self.__grid.get_correct_relative_pos(result)

        if self.__transition.is_mouse_in_screen_transition_area:
            self.__transition.move_camera(result)
            result += self.__transition.transition
            #result = self.__transition.correct_transition(result)
        else:
            self.__transition.nullify_transition()


        result = self.__grid.get_correct_relative_pos(result)

        return result

    def __get_camera_shift_by_mouse(self) -> Point:
        mouse_pos = self.__game.controller.get_mouse_pos()
        mouse_transition = mouse_pos - Point(self.__game.width / 2, self.__game.height / 2)
        return mouse_transition * Camera.MOUSE_SHIFT_SENSIVITY


class CameraTransition:
    """
    Обработчик смещения камеры на значительное расстояние при смещении мыши к краю экрана.
    """
    """
    Какую часть экрана должна занимать область смещения - такая область, нахождение курсора в которой
    начинает смещение.
    (значение должно быть в отрезке [0, 1])
    """
    SCREEN_TRANSITION_AREA_RATIO = 0.1
    """
    Коэффициент максимально смещения экрана (на сколько экранов можно максимально сместить камеру).
    """
    MAXIMUM_TRANSITION_RATIO = 0.4
    """
    Коэффициент скорости смещения экрана (на какую часть экрана должна смещаться камера).
    """
    CAMERA_TRANSITION_SPEED_RATIO = 0.01
    def __init__(self, game, player: Player):
        self.__game = game
        self.__player = player

        self.__transition = Point(0, 0)

    @property
    def is_mouse_in_screen_transition_area(self) -> bool:
        not_transition_area = self.__get_not_transition_area()

        mouse_pos = self.__game.controller.mouse_pos

        return not not_transition_area.is_inside(mouse_pos)

    def move_camera(self, this_camera_pos: Point):
        speed = self.__speed
        direction = self.__get_camera_direction()
        self.__transition += Point(speed.x * direction.x, speed.y * direction.y)
        self.__transition = self.__get_correct_transition(self.__transition, this_camera_pos)

    @property
    def transition(self) -> Point:
        return self.__transition

    def nullify_transition(self):
        self.__transition = Point(0, 0)

    def __get_correct_transition(self, transition, this_camera_pos: Point) -> Point:
        max_value = tuple_to_point(self.__game.size) * CameraTransition.MAXIMUM_TRANSITION_RATIO
        screen_center = tuple_to_point(self.__game.size) / 2
        player_on_screen = self.__player.pos - screen_center
        result = Point(transition.x, transition.y)

        result.x = min(result.x, (player_on_screen.x + max_value.x) - this_camera_pos.x)

        result.x = max(result.x, (player_on_screen.x - max_value.x) - this_camera_pos.x)

        result.y = min(result.y, (player_on_screen.y + max_value.y) - this_camera_pos.y)

        result.y = max(result.y, (player_on_screen.y - max_value.y) - this_camera_pos.y)

        return result

    @property
    def __speed(self) -> Point:
        return tuple_to_point(self.__game.size) * CameraTransition.CAMERA_TRANSITION_SPEED_RATIO

    def __get_camera_direction(self) -> Point:
        mouse_pos = self.__game.controller.mouse_pos
        not_transition_area = self.__get_not_transition_area()

        direction_x = 0

        if mouse_pos.x > not_transition_area.right:
            direction_x = 1
        elif mouse_pos.x < not_transition_area.left:
            direction_x = -1

        direction_y = 0
        if mouse_pos.y > not_transition_area.bottom:
            direction_y = 1
        elif mouse_pos.y < not_transition_area.top:
            direction_y = -1

        return Point(direction_x, direction_y)

    def __get_not_transition_area(self) -> Rectangle:
        w = self.__game.width
        h = self.__game.height
        r = CameraTransition.SCREEN_TRANSITION_AREA_RATIO

        not_transition_area = Rectangle(w * r, h * r, w * (1 - r), h * (1 - r))
        return not_transition_area