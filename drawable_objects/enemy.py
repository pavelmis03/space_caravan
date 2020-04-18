from typing import Optional
import math

from controller.controller import Controller
from drawable_objects.base import Humanoid
from geometry.point import Point
from geometry.vector import length, polar_angle, vector_from_length_angle
from scenes.base import Scene
from drawable_objects.bullet import create_bullet
from geometry.segment import Segment
from geometry.vector import length


class MovingHumanoid(Humanoid):
    """
    Может принимать команду движения к точке
    """
    SPEED = 1

    def _get_move_vector(self, pos: Point) -> Point:
        """
        Получить вектор, на который нужно сдвинуться в этот тик для движения в сторону точки pos.
        """
        """
        Вообще могут быть проблемы из-за correct_direction_vector, так как, делая последний шаг не на максимальный 
        вектор, теряет время. Может быть, не требуется переработка. Может быть, это решается передачей следующей точки.
        """
        self._recount_angle(pos)
        move_vector = vector_from_length_angle(self.SPEED, self.angle)
        result = self.__get_correct_move_vector(move_vector, pos)
        return result

    def __get_correct_move_vector(self, velocity: Point, pos: Point) -> Point:
        """
        Корректирует вектор velocity, на который должен сдвинуться MovingHumanoid к точке pos.

        MovingHumanoid может "перепрыгнуть" точку назначения, поэтому последний прыжок должен быть на меньший вектор.

        :return: корректный вектор.
        """
        remaining_vector = pos - self.pos
        if length(velocity) > length(remaining_vector):
            return remaining_vector
        return velocity

    def _recount_angle(self, new_pos):
        """
        Пересчитать угол по точке, в которую должен направиться MovingHumanoid, и присвоить в self.angle
        """
        vector_to_player = new_pos - self.pos
        self.angle = polar_angle(vector_to_player)


class EnemyCommand:
    """
    Команда, которую Enemy должен выполнить
    """
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

    Рефакторить этот код с паттерном состояние - плохая идея. Проверено на практике.
    """
    IMAGE_ZOOM = 0.3
    IMAGE_NAME = 'moving_objects.enemy2'

    SPEED = 5
    """
    HEARING_RANGE - единица измерения - клетки
    """
    VISION_RADIUS = 20 * 25
    HEARING_RANGE = 35
    AGGRE_RADIUS = 35 * 25

    COOLDOWN_TIME = 50
    DELAY_BEFORE_FIRST_SHOOT = 11

    def __init__(self, scene: Scene, controller: Controller, pos: Point, angle: float = 0):
        super().__init__(scene, controller, Enemy.IMAGE_NAME, pos, angle, Enemy.IMAGE_ZOOM)

        self.__command = None # None означает команду бездействия
        self.__is_see_player = False
        self.__is_aggred = False
        self.__cooldown = 0

        self.__command_functions = {'move_to': self.__command_move_to,
                                  'shoot': self.__command_shoot,
                                  'aim': self.__command_aim, }

    def process_logic(self):
        """
        Логика enemy. Во многом зависит от того, видит он player'а или нет.
        """
        self.__is_see_player = self.scene.grid.is_enemy_see_player(self)
        self.__command_logic()
        if self.__cooldown:
            self.__cooldown -= 1

    def __command_logic(self):
        """
        Логика выполнения той или иной команды, а также получение следующей
        """
        if self.__is_idle:
            self.__command = self.__get_new_command()

        if not self.__is_idle:
            self.__command_functions[self.__command.type](*self.__command.params)

    def __get_new_command(self) -> Optional[EnemyCommand]:
        """
        Получить следующую команду. Обновить self.__is_aggred
        """
        if self.__is_see_player:
            self.__is_aggred = True
            self.__cooldown = max(self.__cooldown, Enemy.DELAY_BEFORE_FIRST_SHOOT)
            return EnemyCommand('aim')

        if self.__is_aggred:
            new_pos = self.scene.grid.get_pos_to_move(self)
            if new_pos is not None:
                self.scene.grid.save_enemy_pos(new_pos) #на случай, если несколько enemy решат пойти в одну клетку
                return EnemyCommand('move_to', new_pos)

        if self.__is_aggred and not self.__is_player_in_aggre_radius:
            self.__is_aggred = False

        return None

    @property
    def __is_idle(self):
        """
        Имеет ли команду или просто бездействует
        """
        return self.__command is None

    def __command_move_to(self, pos: Point):
        """
        Команда движения к точке.
        """
        if pos == self.pos:
            self.__command = None
            """
            рекурсивно вызывать __command_logic может быть плохой идеей. Но это простой способ выбрать следующую 
            команду и выполнить.
            """
            self.__command_logic()
            return

        self.scene.grid.save_enemy_pos(pos)  # на случай, если несколько enemy решат пойти в одну клетку
        self.move(self.pos + self._get_move_vector(pos))

    def __command_shoot(self):
        """
        Команда выстрела в игрока
        """
        self._recount_angle(self.scene.player.pos)

        create_bullet(self)
        self.__cooldown = Enemy.COOLDOWN_TIME

        self.__command = EnemyCommand('aim')

    def __command_aim(self):
        """
        Команда прицеливания в игрока.
        """
        if self.__can_shoot_now:
            self.__command = EnemyCommand('shoot')
            self.__command_logic()
            return

        if not self.__is_see_player:
            self.__command = None
            self.__command_logic()
            return

        self._recount_angle(self.scene.player.pos)

    @property
    def __can_shoot_now(self) -> bool:
        """
        Может ли выстрелить сейчас
        """
        return self.__is_see_player and not self.__cooldown

    @property
    def __is_player_in_aggre_radius(self) -> bool:
        seg = Segment(self.pos, self.scene.player.pos)
        return seg.length < Enemy.AGGRE_RADIUS
