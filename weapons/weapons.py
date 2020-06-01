from typing import Dict
from weapons.base import Weapon, RangedWeapon, MeleeWeapon


class Pistol(RangedWeapon):
    """
    Пистолет
    """
    IMAGE_NAME = 'weapons.pistol'
    DESCRIPTION = """
            Оружие: Пистолет
            Тип: Средние дистанции
            Урон: 45
            Точность: 42
            Интервал стрельбы: 9
            Время перезарядки: 40
            Описание: Ваше первоначальное оружие
                      Вы можете попытаться убить кого-то им, но поищите что-то получше 
            """

    def __init__(self, owner, bullets_in_magazine=12):
        super().__init__(owner, interface_image='interface.weapon_icons.pistol',
                         bullets_in_magazine=bullets_in_magazine, magazine_size=12,
                         main_attack_interval=9, reload_time=40, ammo_type='Pistol',
                         accuracy=42, damage=45)


class BurstFiringPistol(RangedWeapon):
    """
    Стреляющий очередями пистолет
    """
    IMAGE_NAME = 'weapons.burst_firing_pistol'

    DESCRIPTION = """
                Оружие: Пистолет стреляющий очередями
                Тип: Средние дистанции
                Урон: 45
                Точность: 40
                Интервал между очередями: 15
                Время перезарядки: 40
                Описание: 
                """

    def __init__(self, owner, bullets_in_magazine=20):
        super().__init__(owner, interface_image='interface.weapon_icons.burst_firing_pistol',
                         bullets_in_magazine=bullets_in_magazine, magazine_size=20,
                         main_attack_interval=15, reload_time=60, ammo_type='Pistol',
                         accuracy=40, damage=45, combo_attack_interval=3, combo_size=4)


class Shotgun(RangedWeapon):
    """
    Дробовик
    """
    IMAGE_NAME = 'weapons.shotgun'

    DESCRIPTION = """
                Оружие: Дробовик
                Тип: Средние дистанции
                Урон: 50
                Точность: 35
                Интервал стрельбы: 12
                Время перезарядки: 70
                Описание: 
                """

    def __init__(self, owner, bullets_in_magazine=6):
        super().__init__(owner, interface_image='interface.weapon_icons.shotgun',
                         bullets_in_magazine=bullets_in_magazine, magazine_size=6,
                         main_attack_interval=12, reload_time=70, ammo_type='Shotgun',
                         accuracy=35, damage=50, shells=5)


class TwoBarrelShotgun(RangedWeapon):
    """
    Двустволка
    """
    IMAGE_NAME = 'weapons.two_barrel_shotgun'

    DESCRIPTION = """
                Оружие: Двустволка
                Тип: Дальние дистанции
                Урон: 35
                Точность: 32
                Интервал стрельбы: 8
                Время перезарядки: 35
                Описание: 
                """

    def __init__(self, owner, bullets_in_magazine=2):
        super().__init__(owner, interface_image='interface.weapon_icons.two_barrel_shotgun',
                         bullets_in_magazine=bullets_in_magazine, magazine_size=2,
                         main_attack_interval=8, reload_time=35, ammo_type='Shotgun',
                         accuracy=32, damage=35, combo_attack_interval=2, shells=6)
        self.alternative_attack_combo = 2

    def alternative_attack(self):
        if self.cooldown == 0 and self.combo == 0:
            self.combo = self.alternative_attack_combo


class ThreeBarrelShotgun(RangedWeapon):
    """
    Трёхстволка
    """
    IMAGE_NAME = 'weapons.three_barrel_shotgun'

    DESCRIPTION = """
                Оружие: Трёхстволка
                Тип: Средние дистанции
                Урон: 45
                Точность: 42
                Интервал стрельбы: 9
                Время перезарядки: 40
                Описание: 
                """

    def __init__(self, owner, bullets_in_magazine=3):
        super().__init__(owner, interface_image='interface.weapon_icons.three_barrel_shotgun',
                         bullets_in_magazine=bullets_in_magazine, magazine_size=3,
                         main_attack_interval=8, reload_time=35, ammo_type='Shotgun',
                         accuracy=32, damage=35, combo_attack_interval=2, shells=6)
        self.alternative_attack_combo = 3

    def alternative_attack(self):
        if self.cooldown == 0 and self.combo == 0:
            self.combo = self.alternative_attack_combo


class TacticalShotgun(RangedWeapon):
    """
    Тактический дробовик
    """
    IMAGE_NAME = 'weapons.tactical_shotgun'

    DESCRIPTION = """
                Оружие: Тактический дробовик
                Тип: Средние дистанции
                Урон: 45
                Точность: 42
                Интервал стрельбы: 9
                Время перезарядки: 70
                Описание: 
                """

    def __init__(self, owner, bullets_in_magazine=6):
        super().__init__(owner, interface_image='interface.weapon_icons.tactical_shotgun',
                         bullets_in_magazine=bullets_in_magazine, magazine_size=6,
                         main_attack_interval=9, reload_time=70, ammo_type='Shotgun',
                         accuracy=42, damage=45, is_automatic=True, shells=4)


class AutomaticRifle(RangedWeapon):
    """
    Автоматическая винтовка
    """
    IMAGE_NAME = 'weapons.automatic_rifle'

    DESCRIPTION = """
                Оружие: Автоматическая винтовка
                Тип: Средние дистанции
                Урон: 80
                Точность: 60
                Интервал стрельбы: 4
                Время перезарядки: 60
                Описание:  
                """

    def __init__(self, owner, bullets_in_magazine=25):
        super().__init__(owner, interface_image='interface.weapon_icons.automatic_rifle',
                         bullets_in_magazine=bullets_in_magazine, magazine_size=25,
                         main_attack_interval=4, reload_time=60, ammo_type='Rifle',
                         accuracy=60, damage=80, is_automatic=True)


class SniperRifle(RangedWeapon):
    """
    Снайперская винтовка
    """
    IMAGE_NAME = 'weapons.sniper_rifle'

    DESCRIPTION = """
                Оружие: Снайперская винтовка
                Тип: Дальние дистанции
                Урон: 120
                Точность: 110
                Интервал стрельбы: 20
                Время перезарядки: 80
                Описание:  
                """

    def __init__(self, owner, bullets_in_magazine=5):
        super().__init__(owner, interface_image='interface.weapon_icons.sniper_rifle',
                         bullets_in_magazine=bullets_in_magazine, magazine_size=5,
                         main_attack_interval=20, reload_time=80, ammo_type='Rifle',
                         accuracy=110, damage=120)


class OldRifle(RangedWeapon):
    """
    Старая винтовка
    """
    IMAGE_NAME = 'weapons.old_rifle'

    DESCRIPTION = """
                    Оружие: Довоенная винтовка
                    Тип: Дальние дистанции
                    Урон: 90
                    Точность: 90
                    Интервал стрельбы: 14
                    Время перезарядки: 40
                    Описание:  
                    """


    def __init__(self, owner, bullets_in_magazine=8):
        super().__init__(owner, interface_image='interface.weapon_icons.old_rifle',
                         bullets_in_magazine=bullets_in_magazine, magazine_size=8,
                         main_attack_interval=14, reload_time=40, ammo_type='Rifle',
                         accuracy=90, damage=90)


class SemiAutomaticRifle(RangedWeapon):
    """
    Полуавтоматическая винтовка
    """
    IMAGE_NAME = 'weapons.semi_automatic_rifle'

    DESCRIPTION = """
                    Оружие: Полуавтоматическая винтовка
                    Тип: Дальние дистанции
                    Урон: 120
                    Точность: 60
                    Интервал стрельбы: 10
                    Время перезарядки: 50
                    Описание:  
                    """

    def __init__(self, owner, bullets_in_magazine=8):
        super().__init__(owner, interface_image='interface.weapon_icons.semi_automatic_rifle',
                         bullets_in_magazine=bullets_in_magazine, magazine_size=8,
                         main_attack_interval=9, reload_time=50, ammo_type='Rifle',
                         accuracy=60, damage=90)


class Sword(MeleeWeapon):
    """
    Меч
    """
    IMAGE_NAME = 'other.gun'

    DESCRIPTION = """
                        Оружие: Меч
                        Тип: Ближние дистанции
                        Урон: 999
                        Точность: 999
                        Интервал удара: 15
                        Время перезарядки: ОНА ЕМУ НЕ НУЖНА
                        Описание:  
                        """

    def __init__(self, owner):
        super().__init__(owner, interface_image='other.gun',
                         main_attack_interval=15, length=60)


class Fist(MeleeWeapon):
    """
    Кулак(персонаж бьёт только одним)
    """
    DESCRIPTION = """
                            Оружие: братиш, у тебя его нет
                            Тип: угу
                            Урон: 25
                            Точность: ну так себе
                            Интервал удара: 7
                            Время перезарядки: ручки быстро устают
                            Описание:  
                            """

    def __init__(self, owner):
        super().__init__(owner, interface_image='interface.weapon_icons.nothing',
                         main_attack_interval=7, length=40)

    def attack(self):
        """
        Функция атаки
        """
        from drawable_objects.slash import Punch
        # SoundManager.play_sound('weapon.shoot')
        self.scene.game_objects.append(Punch(self.owner, self.length))


WEAPON_VOCABULARY = {
    'Pistol': Pistol, #tier1
    'BurstFiringPistol': BurstFiringPistol, #t3
    'Shotgun': Shotgun, #t3
    'TwoBarrelShotgun': TwoBarrelShotgun, #t1
    'ThreeBarrelShotgun': ThreeBarrelShotgun, #t2
    'TacticalShotgun': TacticalShotgun, #t3.5
    'AutomaticRifle': AutomaticRifle, #t2.5
    'SniperRifle': SniperRifle, #t2.5
    'OldRifle': OldRifle, #t1
    'SemiAutomaticRifle': SemiAutomaticRifle, #t2
    'Sword': Sword, #t?
    'Fist': Fist,
}


WEAPON_ON_FLOOR_IMAGE = {
    'Pistol': 'weapons_on_floor.pistol',
    'BurstFiringPistol': 'weapons_on_floor.burst_firing_pistol',
    'Shotgun': 'weapons_on_floor.shotgun',
    'TwoBarrelShotgun': 'weapons_on_floor.two_barrel_shotgun',
    'ThreeBarrelShotgun': 'weapons_on_floor.three_barrel_shotgun',
    'TacticalShotgun': 'weapons_on_floor.tactical_shotgun',
    'AutomaticRifle': 'weapons_on_floor.automatic_rifle',
    'SniperRifle': 'weapons_on_floor.sniper_rifle',
    'OldRifle': 'weapons_on_floor.old_rifle',
    'SemiAutomaticRifle': 'weapons_on_floor.semi_automatic_rifle',
    'Sword': 'other.gun',
}


def weapon_to_dict(weapon: Weapon) -> Dict:
    """
    работает за O(weapons.weapons.WEAPON_VOCABULARY), но
    в высокой скорости нет необходимости
    """
    for key, value in WEAPON_VOCABULARY.items():
        if not isinstance(weapon, value):
            continue

        result = {'weapon': key}
        if weapon.type == 'Ranged':
            result.update({'magazine': weapon.magazine})
        return result

    raise Exception('Weapon does not exist')
