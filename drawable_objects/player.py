from typing import List
from geometry.point import Point
import pygame
from drawable_objects.base import Humanoid
from geometry.point import Point
from geometry.vector import sign, length, normalized, polar_angle
from geometry.rectangle import Rectangle
from geometry.distances import vector_dist_point_rect
from constants.directions import DIRECTIONS
from scenes.base import Scene
from controller.controller import Controller
from drawable_objects.bullet import create_bullet
from weapons.weapons import Pistol
from weapons.weapons import Shotgun


class Player(Humanoid):
    """
    Игрок на уровне (далек от завершения).

    :param scene: сцена, на которой находится игрок
    :param controller: контроллер
    :param pos: начальная позиция игрока
    :param angle: начальный угол поворота игрока
    """

    IMAGE_NAME = 'moving_objects.player'
    IMAGE_ZOOM = 0.25
    CONTROLS = [
        pygame.K_d,
        pygame.K_w,
        pygame.K_a,
        pygame.K_s,
    ]
    SPEED = 10

    def __init__(self, scene: Scene, controller: Controller, pos: Point, angle: float = 0):
        super().__init__(scene, controller, Player.IMAGE_NAME, pos, angle, Player.IMAGE_ZOOM)
        # head - 140x126
        self.rotation_offset = [
            140 * Player.IMAGE_ZOOM,
            126 * Player.IMAGE_ZOOM
        ]

        self.weapon = Shotgun(self, 100, 6)
        self.scene.interface_objects.append(self.weapon)

    def process_logic(self):
        relative_center = self.scene.relative_center
        vector_to_mouse = self.controller.get_mouse_pos() + relative_center - self.pos
        self.angle = polar_angle(vector_to_mouse)
        velocity = Point()
        if self in self.controller.input_objects:
            for i in range(4):
                if self.controller.is_key_pressed(Player.CONTROLS[i]):
                    velocity += DIRECTIONS[i]
            velocity *= self.SPEED

        new_pos = self.go_from_walls(self.pos + velocity)
        if sign(length(new_pos - self.pos - velocity)) != 0:
            new_pos = self.go_from_walls(self.pos + velocity)
        self.move(new_pos)

    def go_from_walls(self, player_pos: Point) -> Point:
        """
        Вытаскивание игрока из стен.

        :param player_pos: позиция игрока
        :return: позиция игрока после выталкивания из стен
        """
        result_pos = Point(player_pos.x, player_pos.y)
        collision_rects = self.scene.grid.get_collision_rects_nearby(player_pos)
        while True:
            vectors = self._get_vectors_to_intersected_rects(result_pos, collision_rects)
            if len(vectors) == 0:
                break
            min_vector = self._get_min_vector(vectors)
            push_vector = self._get_push_vector(min_vector)
            result_pos += push_vector
        return result_pos

    def _get_push_vector(self, vector_to_wall: Point) -> Point:
        """
        Получить вектор выталкивания
        """
        intersection_distance = self.HITBOX_RADIUS - length(vector_to_wall)
        direction_vector = normalized(vector_to_wall)
        return direction_vector * intersection_distance

    def _get_min_vector(self, vectors: List[Point]) -> Point:
        """
        Получить минимальный по длине вектор
        """
        result = vectors[0]
        for i in range(1, len(vectors)):
            if length(vectors[i]) < length(result):
                result = vectors[i]
        return result

    def _get_vectors_to_intersected_rects(self, pos: Point, rects: List[Rectangle]) -> List[Point]:
        """
        Проверяет расстояния от центра хитбокса до блоков стен, и если какое-то из них меньше радиуса, добавляет
        в список.
        """
        result = []
        for rect in rects:
            vector_to_rect = vector_dist_point_rect(pos, rect)
            if sign(self.HITBOX_RADIUS - length(vector_to_rect)) == 1:
                result.append(vector_to_rect)
        return result
