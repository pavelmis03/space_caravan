from drawable_objects.base import GameSprite
from drawable_objects.bullet import BULLET_CLASS
from geometry.segment import Segment
from geometry.vector import vector_from_length_angle
from geometry.point import Point
from utils.sound import SoundManager
from random import randrange
from drawable_objects.slash import PlayerSlash, EnemySlash


class Weapon(GameSprite):
    IMAGE_NAME = 'weapons.gun'
    DESCRIPTION = """
                Оружие: 
                Тип: 
                Урон: 
                Точность: 
                Интервал стрельбы: 
                Время перезарядки: 
                Описание: 
                """

    def __init__(self, owner, interface_image, main_attack_interval,
                 is_automatic=False, combo_attack_interval=0, combo_size=1):
        """
        :param owner: DrawableObject, имеющий оружие -> DrawableObject
        :param scene_image: картинка на сцене
        :param interface_image: картинка в интерфейсе(в слотах оружия)
        :param main_attack_interval: Время между выстрелами -> int
        :param is_automatic: Автоматическое ли оружие -> bool
        :param combo_attack_interval: Интервал между ударами/выстрелами в 1 атаке -> int
        :param combo_size: Количество ударов/выстрелов в 1 атаке -> int
        """
        self.owner = owner
        self.interface_image = interface_image
        super().__init__(owner.scene, owner.controller, self.IMAGE_NAME,
                         self.owner.pos, self.owner.angle, 0.5)
        self.is_automatic = is_automatic
        self.main_attack_interval = main_attack_interval
        self.combo_attack_interval = combo_attack_interval
        self.combo = 0
        self.combo_size = combo_size
        self.cooldown = 0
        self.type = ''

    def process_logic(self):
        self.pos = self.owner.pos
        self.angle = self.owner.angle
        if self.cooldown:
            self.cooldown -= 1
        if self.combo != 0 and self.cooldown == 0:
            self.combo -= 1
            if self.combo == 0:
                self.cooldown = self.main_attack_interval
            else:
                self.cooldown = self.combo_attack_interval
            self.attack()

    def process_draw(self):
        self.pos = self.owner.pos
        self.angle = self.owner.angle
        super().process_draw()

    def main_attack(self):
        """
        Команда оружию атаковать
        """
        if self.cooldown == 0 and self.combo == 0:
            self.combo = self.combo_size

    def alternative_attack(self):
        """
        Команда оружию атаковать альтернативно
        """

    def attack(self):
        """
        Функция атаки
        """

    @property
    def is_fired_this_tick(self):
        """
        Издало ли оружие звук в этот тик(чтобы Enemy слышали)
        """
        return False


class RangedWeapon(Weapon):

    SHOOT_SOUND = 'weapon.attack.default'
    RELOAD_SOUND = 'weapon.reload.pistol'

    def __init__(self, owner, interface_image, bullets_in_magazine, magazine_size, main_attack_interval,
                 reload_time, ammo_type, accuracy, damage,
                 is_automatic=False, shells=1, combo_attack_interval=0, combo_size=1):
        """
        :param owner: DrawableObject, имеющий оружие -> DrawableObject
        :param scene_image: картинка на сцене
        :param interface_image: картинка в интерфейсе(в слотах оружия)
        :param bullets_in_magazine: Сколько пуль в магазине на момент получения оружия -> int
        :param magazine_size: Размер магазина -> int
        :param main_attack_interval: Время между атаками -> int
        :param reload_time: Время перезарядки -> int
        :param ammo_type: Вид пули -> string
        :param accuracy: Точноcть -> int
        :param damage: Урон -> int
        :param is_automatic: Автоматическое ли оружие -> bool
        :param shells: Количество Bullet, вылетающих из оружия при одном выстреле -> int
        :param combo_attack_interval: Интервал между выстрелами в очереди -> int
        :param combo_size: Длина очереди -> int
        """
        super().__init__(owner, interface_image, main_attack_interval, is_automatic,
                         combo_attack_interval, combo_size)
        self.zoom = 1.15
        self.reload_time = reload_time
        self.is_reloading = 0
        self.reload_request = False
        self.barrel_length = owner.HITBOX_RADIUS + 1
        self.magazine_size = magazine_size
        self.magazine = bullets_in_magazine
        self.ammo = 0
        self.ammo_type = ammo_type
        self.accuracy = accuracy
        self.damage = damage
        self.shells = shells
        self.type = 'Ranged'
        self._is_fired_this_tick = False
        if self.is_automatic and self.owner.__class__.__name__ == 'Enemy' and self.main_attack_interval < 8 and\
                self.combo_size == 1:
            self.combo_size = 1 + 10 // self.main_attack_interval
            self.combo_attack_interval = self.main_attack_interval

    def reload(self):
        """
        Функция перезарядки
        """
        self.combo = 0
        if self.magazine == self.magazine_size or self.ammo == 0:
            self.reload_request = False
            return
        if not self.is_reloading:
            SoundManager.play_sound(self.RELOAD_SOUND)
            self.is_reloading = self.reload_time
            self.cooldown = self.reload_time

    def end_reloading(self):
        """
        Делает всё, что нужно после перезарядки
        """
        self.reload_request = False
        ammo_to_add = min(self.ammo, self.magazine_size - self.magazine)
        self.magazine += ammo_to_add
        self.ammo -= ammo_to_add
        self.owner.ammo[self.ammo_type] -= ammo_to_add

    def process_logic(self):
        self.ammo = self.owner.ammo[self.ammo_type]
        if self.is_reloading:
            self.is_reloading -= 1
            if not self.is_reloading:
                self.end_reloading()
        self._is_fired_this_tick = False
        super().process_logic()
        if self.reload_request and not self.is_reloading and self.combo == 0:
            self.reload()

    def attack(self):
        """
        Функция атаки
        """
        if self.magazine == 0:
            self.cooldown = 0
            self.reload()
            return
        if self.owner.__class__.__name__ == 'Player':
            self._is_fired_this_tick = True
        self.magazine -= 1
        SoundManager.play_sound(self.SHOOT_SOUND)
        end_of_the_barrel = self.owner.pos + vector_from_length_angle(self.barrel_length, self.owner.angle)
        if self.scene.grid.intersect_seg_walls(Segment(self.owner.pos, end_of_the_barrel)) is None:
            self.shot(end_of_the_barrel, self.owner.angle)

    def shot(self, pos: Point, angle: float):
        """
        Функция выстрела(вынесена из attack, чтобы не захламлять код)

        :param pos: откуда производится выстрел -> Point
        :param angle: под каким углом производится выстрел -> float
        """
        for _ in range(self.shells):
            bullet = BULLET_CLASS[self.ammo_type](self, pos, angle + randrange(-100, 100) /
                                                  (self.accuracy ** 2 - self.accuracy * 20 + 100), self.damage)
            self.scene.game_objects.append(bullet)

    @property
    def is_fired_this_tick(self):
        """
        Издало ли оружие звук в этот тик(чтобы Enemy слышали)
        """
        return self._is_fired_this_tick


class MeleeWeapon(Weapon):
    ATTACK_SOUND = 'weapon.attack.sword'

    def __init__(self, owner, interface_image, main_attack_interval, length):
        """
        :param owner: DrawableObject, имеющий оружие -> DrawableObject
        :param scene_image: картинка на сцене
        :param interface_image: картинка в интерфейсе(в слотах оружия)
        :param main_attack_interval: Время между взмахами -> int
        :param length: Длина клинка -> int
        """
        super().__init__(owner, interface_image, main_attack_interval)
        self.zoom = 1.15
        self.length = owner.HITBOX_RADIUS + length
        self.type = 'Melee'

    def attack(self):
        """
        Функция атаки
        """
        SoundManager.play_sound(self.ATTACK_SOUND)
        if self.owner.__class__.__name__ == 'Player':
            self.scene.game_objects.append(PlayerSlash(self.owner, self.length))
        else:
            self.scene.game_objects.append(EnemySlash(self.owner, self.length))

    def process_draw(self):
        if self.owner.__class__.__name__ != 'Player' and self.owner.__class__.__name__ != 'Enemy' and \
                self.owner.__class__.__name__ != 'SoullessPlayer':
            super().process_draw()