import math

from controller.controller import Controller
from drawable_objects.base import Humanoid
from geometry.point import Point
from geometry.vector import length, polar_angle, vector_from_length_angle
from scenes.base import Scene
from drawable_objects.bullet import create_bullet


class MovingHumanoid(Humanoid):
    """
    Может принимать команду движения к точке
    """
    SPEED = 1

    def get_move_vector(self, pos: Point):
        """
        вообще могут быть проблемы из-за correct_direction_vector, так
        как, делая последний шаг не на максимальный вектор,
        теряет время. Может быть, не требуется переработка.
        Может быть, это решается передачей следующией команды.
        """
        self.recount_angle(pos)
        direction = vector_from_length_angle(self.SPEED, self.angle)
        result = self.correct_direction_vector(direction, pos)
        return result

    def correct_direction_vector(self, velocity: Point, pos: Point):
        """
        Humanoid может "перепрыгнуть" точку назначения, поэтому
        последний прыжок должен быть на меньший вектор
        """
        remaining_vector = pos - self.pos
        if length(velocity) > length(remaining_vector):
            return remaining_vector
        return velocity

    def recount_angle(self, new_pos):
        vector_to_player = new_pos - self.pos
        self.angle = polar_angle(vector_to_player)


class EnemyCommand:
    def __init__(self, type: str, *params):
        self.type = type
        self.params = params


class Enemy(MovingHumanoid):
    """
    Сейчас он ведет себя следующим образом:
    Стоит на месте. Когда игрок попадает в радиус видимости и их не разделяет стена, начинает стрелять.
    Если выстрелить становится нельзя, преследует игрока, пока он находится в радиусе слышимости.
    Если игрок стал находиться вне радиуса слышимости, стоит на месте.

    Еще нет коллизий с пулей.
    """
    IMAGE_ZOOM = 0.3
    IMAGE_NAME = 'enemy2'

    SPEED = 5
    """
    VISION_RADIUS не должен быть большим, так
    как grid.intersect_seg_walls работает медленно  
    """
    VISION_RADIUS = 25 * 15
    HEARING_RANGE = 30
    COOLDOWN_TIME = 50

    def __init__(self, scene: Scene, controller: Controller, pos: Point, angle: float = 0):
        super().__init__ (scene, controller, Enemy.IMAGE_NAME, pos, angle, Enemy.IMAGE_ZOOM)

        self.is_has_command = False
        self.command = None
        self.is_aggred = False
        self.cooldown = 0

        self.command_functions = {'move_to': self.command_move_to,
                                  'shoot': self.command_shoot,
                                  'aim': self.command_aim,}

    def command_move_to(self, pos: Point):
        if pos == self.pos:
            self.is_has_command = False
            """
            рекурсивно вызывать command_logic может быть
            плохой идеей.
            """
            self.command_logic()
            return

        self.move(self.pos + self.get_move_vector(pos))

    def command_shoot(self):
        self.recount_angle(self.scene.player.pos)

        create_bullet(self)
        self.cooldown = Enemy.COOLDOWN_TIME

        self.command = EnemyCommand('aim')

    def command_aim(self):
        """
        Возможно, следует переработать, чтобы он
         сначала целился какое-то время, а потом делал первый выстрел.
        """
        if not self.is_see_player or self.can_shoot_now:
            self.is_has_command = False
            self.command_logic()
            return

        self.recount_angle(self.scene.player.pos)

    @property
    def can_shoot_now(self):
        return self.is_see_player and not self.cooldown

    def create_new_command(self):
        if self.can_shoot_now:
            self.is_aggred = True
            self.is_has_command = True
            self.command = EnemyCommand('shoot')
        elif self.is_aggred:
            new_pos = self.scene.grid.get_pos_to_move(self)
            if new_pos is None:
                self.is_aggred = False
                return
            self.is_has_command = True
            self.command = EnemyCommand('move_to', new_pos)

    def command_logic(self):
        if not self.is_has_command:
            self.create_new_command()

        if self.is_has_command:
            self.command_functions[self.command.type](*self.command.params)

    def process_logic(self):
        self.is_see_player = self.scene.grid.is_enemy_see_player(self)
        self.command_logic()
        if self.cooldown:
            self.cooldown -= 1