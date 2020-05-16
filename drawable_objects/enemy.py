import weapons.weapons
#from weapons.weapons import WEAPON_VOCABULARY - это единственное, что тут нужно из weapons

from typing import Optional

from controller.controller import Controller
from drawable_objects.base import Humanoid
from geometry.point import Point
from geometry.vector import polar_angle, vector_from_length_angle
from scenes.base import Scene
from geometry.segment import Segment
from geometry.vector import length
from random import randint
from utils.random import is_random_proc
from math import pi
from utils.timer import Timer, EMPTY_TIMER


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


class CommandHumanoid(MovingHumanoid):
    """
    Humanoid, которые следует командам. Скорее всего, нужен только для того, чтобы от него наследовался Enemy.
    Переносить код отсюда в Enemy не стоит, т.к. класс и так огромный.

    Сейчас он ведет себя следующим образом:
    Стоит на месте. Когда игрок попадает в радиус видимости и их не разделяет стена, начинает стрелять.
    Если выстрелить становится нельзя, преследует игрока, пока он находится в радиусе слышимости.
    Если игрок стал находиться вне радиуса слышимости, стоит на месте.

    Еще нет коллизий с пулей.

    Рефакторить этот код с паттерном состояние - плохая идея. Проверено на практике.
    """

    ADD_TO_GAME_PLANE = True
    SPEED = 9

    """
    HEARING_RANGE - единица измерения - клетки
    """
    VISION_RADIUS = 25 * 25
    VIEW_ANGLE = pi #с углом > pi работать не будет

    HEARING_RANGE = 35
    AGGRE_RADIUS = 35 * 25

    COOLDOWN_TIME = 50
    DELAY_BEFORE_FIRST_SHOOT = 12
    DELAY_BEFORE_HEARING = 8

    def __init__(self, scene: Scene, controller: Controller, image_name: str, pos: Point, angle: float,
                 image_zoom: float):
        super().__init__(scene, controller, image_name, pos, angle, image_zoom)

        self.__command = None # None означает команду бездействия
        self.__is_see_player = False
        self._is_aggred = False
        self.__cooldown = 0
        self.__hearing_timer_delay = EMPTY_TIMER #задержка перед реакцией enemy на выстрел

        self.ammo = {
            'Pistol': 1000000,
            'Shotgun': 1000000,
            'Rifle': 1000000,
        }
        self.weapon = weapons.weapons.WEAPON_VOCABULARY['BurstFiringPistol'](self)
        self.scene.game_objects.append(self.weapon)
        self.hp = 100

        self.__command_functions = {'move_to': self.__command_move_to,
                                  'shoot': self.__command_shoot,
                                  'aim': self.__command_aim, }

    def process_logic(self):
        """
        Логика enemy. Во многом зависит от того, видит он player'а или нет.
        """
        self.__vision_logic()
        self.__hearing_logic()
        self.__command_logic()
        if self.__cooldown:
            self.__cooldown -= 1

    def __vision_logic(self):
        """
        Логика зрения Enemy
        """
        self.__is_see_player = self.scene.grid.is_enemy_see_player(self)

    def __hearing_logic(self):
        """
        Логика слуха Enemy
        """
        self.__hearing_timer_logic()

        if not self.scene.player.is_fired_this_tick:
            return

        # если timer не started, то это значит, что сейчас используется пустой таймер и можно начать новый.
        if not self.__hearing_timer_delay.is_started and self.scene.grid.is_hearing_player(self):
            self.__hearing_timer_delay = Timer(Enemy.DELAY_BEFORE_HEARING)
            self.__hearing_timer_delay.start()

    def __hearing_timer_logic(self):
        self.__hearing_timer_delay.process_logic()
        if self.__hearing_timer_delay.is_alarm:
            self._is_aggred = True
            self.__hearing_timer_delay = EMPTY_TIMER

    def __command_logic(self):
        """
        Логика выполнения той или иной команды, а также получение следующей
        """
        if self._is_idle:
            self.__command = self.__get_new_command()

        if not self._is_idle:
            self.__command_functions[self.__command.type](*self.__command.params)

    def __get_new_command(self) -> Optional[EnemyCommand]:
        """
        Получить следующую команду. Обновить self.__is_aggred
        """
        if self.__is_see_player:
            self._is_aggred = True
            self.__cooldown = max(self.__cooldown, CommandHumanoid.DELAY_BEFORE_FIRST_SHOOT)
            return EnemyCommand('aim')

        if self._is_aggred:
            new_pos = self.scene.grid.get_pos_to_move(self)
            if new_pos is not None:
                self.scene.grid.save_enemy_pos(new_pos) #на случай, если несколько enemy решат пойти в одну клетку
                return EnemyCommand('move_to', new_pos)

        if self._is_aggred and not self.__is_player_in_aggre_radius:
            self._is_aggred = False

        return None

    @property
    def _is_idle(self):
        """
        Имеет ли команду или просто бездействует
        """
        return self.__command is None

    def __command_move_to(self, pos: Point):
        """
        Команда движения к точке.
        """
        self.scene.grid.save_enemy_pos(pos)  # на случай, если несколько enemy решат пойти в одну клетку

        if pos == self.pos:
            self.__command = None
            """
            рекурсивно вызывать __command_logic может быть плохой идеей. Но это простой способ выбрать следующую 
            команду и выполнить.
            """
            self.__command_logic()
            return

        self.move(self.pos + self._get_move_vector(pos))

    def __command_shoot(self):
        """
        Команда выстрела в игрока
        """
        self._recount_angle(self.scene.player.pos)

        self.weapon.main_attack()
        if self.weapon.type == 'Ranged' and self.weapon.magazine == 0:
            self.weapon.reload()

        self.__cooldown = CommandHumanoid.COOLDOWN_TIME
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
        """
        Находится ли игрок в радиусе слышимости.

        Проверяет, находится ли игрок в квадрате со стороной AGGRE_RADIUS и
        центром в enemy.pos.
        """
        """
        Проверка через евклидово расстояние не подходит, т.к. aggre_radius должен совпадать с
        радиусом слышимости, а он рассчитывается bfs'ом, в результате которого получается квадрат, 
        а не круг (если игнорировать стены).
        """
        distance_x = abs(self.pos.x - self.scene.player.pos.x)
        distance_y = abs(self.pos.y - self.scene.player.pos.y)
        return distance_x < CommandHumanoid.AGGRE_RADIUS and \
               distance_y < CommandHumanoid.AGGRE_RADIUS


class Enemy(CommandHumanoid):
    """
    Основной противник в Dungeon.
    """

    IMAGE_ZOOM = 0.3
    IMAGE_NAME = 'moving_objects.enemy2'

    ANGULAR_VELOCITY = 6 / 65

    ROTATION_TIME = 40 #количество циклов поворота
    ROTATION_MIN_COOLDOWN = 100
    ROTATION_MAX_COOLDOWN = 250
    ROTATION_CHANGE_DIRECTION_CHANCE = 30
    def __init__(self, scene: Scene, controller: Controller, pos: Point = Point(), angle: float = 0):
        super().__init__(scene, controller, Enemy.IMAGE_NAME, pos, angle, Enemy.IMAGE_ZOOM)
        self.__rotate_cooldown = randint(Enemy.ROTATION_MIN_COOLDOWN, Enemy.ROTATION_MAX_COOLDOWN)
        self.__rotation_direction = 1 if is_random_proc() else -1
        self.__rotating_cycles = 0

    def process_logic(self):
        """
        Добавлена логика поворота
        """
        if not self.enabled:
            return
        super().process_logic()
        if self._is_idle and not self._is_aggred:
            self.__rotation_logic()

    def __rotation_logic(self):
        """
        Логика поворота.
        """
        if not self.__is_rotating:
            self.__rotate_cooldown -= 1
            return

        if self.__is_just_start_rotation:
            self.__choose_direction()

        self.__rotation_tic()

        if self.__is_should_end_rotation:
            self.__end_rotation()

    def __choose_direction(self):
        """
        Меняет направление поворота с вероятностью Enemy.ROTATION_CHANGE_DIRECTION_CHANCE
        """
        if is_random_proc(Enemy.ROTATION_CHANGE_DIRECTION_CHANCE):
            self.__rotation_direction *= -1

    def __rotation_tic(self):
        """
        Тик поворота.
        """
        self.angle += Enemy.ANGULAR_VELOCITY * self.__rotation_direction
        self.__rotating_cycles += 1

    @property
    def __is_should_end_rotation(self):
        """
        Нужно ли прекратить поворачиваться
        """
        return self.__rotating_cycles == Enemy.ROTATION_TIME

    def __end_rotation(self):
        """
        Закончить поворот
        """
        self.__rotating_cycles = 0
        self.__rotate_cooldown = randint(Enemy.ROTATION_MIN_COOLDOWN, Enemy.ROTATION_MAX_COOLDOWN)

    @property
    def __is_rotating(self):
        """
        Поворачивается ли сейчас
        """
        return self.__rotate_cooldown == 0

    @property
    def __is_just_start_rotation(self):
        """
        Только ли начал поворачиваться
        """
        return self.__rotating_cycles == 0

    def get_damage(self, damage=0, angle_of_attack=0):
        """
        Получение урона

        :param damage: урон
        :param angle_of_attack: угол, под которым Enemy ударили(для анимаций)
        """
        self.hp -= damage
        if self.hp <= 0:
            self.die(angle_of_attack)

    def die(self, angle_of_attack=0):
        """
        Смээээрть

        :param angle_of_attack: угол, под которым Enemy ударили(для анимаций)
        """
        self.weapon.destroy()
        self.destroy()
