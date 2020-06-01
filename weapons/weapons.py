from typing import Dict
from weapons.base import Weapon, RangedWeapon, MeleeWeapon


class Pistol(RangedWeapon):
    """
    Пистолет
    """
    IMAGE_NAME = 'other.gun'
    def __init__(self, owner, bullets_in_magazine=12):
        super().__init__(owner, interface_image='interface.weapon_icons.Pistol',
                         bullets_in_magazine=bullets_in_magazine, magazine_size=12,
                         main_attack_interval=9, reload_time=40, ammo_type='Pistol',
                         accuracy=42, damage=45)


class BurstFiringPistol(RangedWeapon):
    """
    Стреляющий очередями пистолет
    """
    IMAGE_NAME = 'other.gun'
    def __init__(self, owner, bullets_in_magazine=20):
        super().__init__(owner, interface_image='interface.weapon_icons.TwoBarrelShotgun',
                         bullets_in_magazine=bullets_in_magazine, magazine_size=20,
                         main_attack_interval=15, reload_time=60, ammo_type='Pistol',
                         accuracy=40, damage=45, combo_attack_interval=3, combo_size=4)


class Shotgun(RangedWeapon):
    """
    Дробовик
    """
    IMAGE_NAME = 'other.gun'
    def __init__(self, owner, bullets_in_magazine=6):
        super().__init__(owner, interface_image='other.gun',
                         bullets_in_magazine=bullets_in_magazine, magazine_size=6,
                         main_attack_interval=12, reload_time=70, ammo_type='Shotgun',
                         accuracy=35, damage=50, shells=5)


class TwoBarrelShotgun(RangedWeapon):
    """
    Двустволка
    """
    IMAGE_NAME = 'other.gun'
    def __init__(self, owner, bullets_in_magazine=2):
        super().__init__(owner, interface_image='interface.weapon_icons.TwoBarrelShotgun',
                         bullets_in_magazine=bullets_in_magazine, magazine_size=2,
                         main_attack_interval=8, reload_time=35, ammo_type='Shotgun',
                         accuracy=32, damage=35, combo_attack_interval=2, shells=6)
        self.alternative_attack_combo = 2

    def alternative_attack(self):
        if self.cooldown == 0 and self.combo == 0:
            self.combo = self.alternative_attack_combo


class ThreeBarrelShotgun(TwoBarrelShotgun):
    """
    Трёхстволка
    """
    IMAGE_NAME = 'other.gun'
    def __init__(self, owner, bullets_in_magazine=3):
        super().__init__(owner, bullets_in_magazine)
        self.image_name = 'other.gun'
        self.interface_image = 'other.gun'
        self.magazine_size = 3
        self.alternative_attack_combo = 3


class TacticalShotgun(RangedWeapon):
    """
    Тактический дробовик
    """
    IMAGE_NAME = 'other.gun'
    def __init__(self, owner, bullets_in_magazine=6):
        super().__init__(owner, interface_image='other.gun',
                         bullets_in_magazine=bullets_in_magazine, magazine_size=6,
                         main_attack_interval=9, reload_time=70, ammo_type='Shotgun',
                         accuracy=42, damage=45, is_automatic=True, shells=4)


class AutomaticRifle(RangedWeapon):
    """
    Автоматическая винтовка
    """
    IMAGE_NAME = 'other.gun'

    def __init__(self, owner, bullets_in_magazine=25):
        super().__init__(owner, interface_image='other.gun',
                         bullets_in_magazine=bullets_in_magazine, magazine_size=25,
                         main_attack_interval=4, reload_time=60, ammo_type='Rifle',
                         accuracy=60, damage=80, is_automatic=True)


class SniperRifle(RangedWeapon):
    """
    Снайперская винтовка
    """
    IMAGE_NAME = 'other.gun'
    def __init__(self, owner, bullets_in_magazine=5):
        super().__init__(owner, interface_image='other.gun',
                         bullets_in_magazine=bullets_in_magazine, magazine_size=5,
                         main_attack_interval=20, reload_time=80, ammo_type='Rifle',
                         accuracy=110, damage=120)


class OldRifle(RangedWeapon):
    """
    Старая винтовка
    """
    IMAGE_NAME = 'other.gun'

    def __init__(self, owner, bullets_in_magazine=8):
        super().__init__(owner, interface_image='other.gun',
                         bullets_in_magazine=bullets_in_magazine, magazine_size=8,
                         main_attack_interval=14, reload_time=40, ammo_type='Rifle',
                         accuracy=90, damage=90)


class SemiAutomaticRifle(OldRifle):
    """
    Полуавтоматическая винтовка
    """
    IMAGE_NAME = 'other.gun'

    def __init__(self, owner, bullets_in_magazine=8):
        super().__init__(owner, bullets_in_magazine)
        self.image_name = self.IMAGE_NAME
        self.scene_image = 'other.gun'
        self.main_attack_interval = 10
        self.reload_time = 50
        self.accuracy = 60


class Sword(MeleeWeapon):
    IMAGE_NAME = 'other.gun'

    def __init__(self, owner):
        super().__init__(owner, interface_image='other.gun',
                         main_attack_interval=15, length=60)


class Fist(MeleeWeapon):
    IMAGE_NAME = 'other.bullet'

    def __init__(self, owner):
        super().__init__(owner, interface_image='other.bullet',
                         main_attack_interval=7, length=30)

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


def weapon_to_dict(weapon: Weapon) -> Dict:
    '''
    работает за O(weapons.weapons.WEAPON_VOCABULARY), но
    в высокой скорости нет необходимости
    '''
    for key, value in WEAPON_VOCABULARY.items():
        if not isinstance(weapon, value):
            continue

        result = {'weapon': key}
        if weapon.type == 'Ranged':
            result.update({'magazine': weapon.magazine})
        return result

    raise Exception('Weapon does not exist')
