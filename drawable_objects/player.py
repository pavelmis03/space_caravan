import pygame

from drawable_objects.base import Humanoid
from geometry.point import Point
from geometry.vector import sign, length, normalized, polar_angle
from geometry.distances import vector_dist_point_rect
from constants.directions import DIRECTIONS
from scenes.base import Scene
from controller.controller import Controller

from drawable_objects.bullet import create_bullet


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
        self.time = 0
        super().__init__(scene, controller, Player.IMAGE_NAME, pos, angle, Player.IMAGE_ZOOM)
        # head - 140x126
        self.rotation_offset = [
            140 * Player.IMAGE_ZOOM,
            126 * Player.IMAGE_ZOOM
        ]

    def process_logic(self):
        relative_center = self.scene.relative_center
        vector_to_mouse = self.controller.get_mouse_pos() + relative_center - self.pos
        self.angle = polar_angle(vector_to_mouse)

        if self.controller.get_click_button():
            create_bullet(self)

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

    def go_from_walls(self, p: Point) -> Point:
        """
        Вытаскивание игрока из стен. Проверяет расстояния от центра хитбокса до блоков стен, и если какое-то из них
        меньше радиуса, то происходит выталкивание по вектору этого расстояния. Это повторяется, пока игрок не выйдет
        из стены.

        :param p: позиция игрока
        :return: позиция игрока после выталкивания из стен
        """
        pos = Point(p.x, p.y)
        rects = self.scene.grid.get_collision_rects_nearby(pos)
        while True:
            v = []
            for rect in rects:
                current_v = vector_dist_point_rect(pos, rect)
                if sign(self.HITBOX_RADIUS - length(current_v)) == 1:
                    v.append(current_v)
            if len(v) == 0:
                break
            for i in range(1, len(v)):
                if length(v[0]) > length(v[i]):
                    v[0], v[i] = v[i], v[0]
            push_v = normalized(v[0]) * (self.HITBOX_RADIUS - length(v[0]))
            pos += push_v
        return pos
