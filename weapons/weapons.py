from weapons.base import RangedWeapon, MeleeWeapon


class Pistol(RangedWeapon):
    """
    Пистолет
    """

    def __init__(self, owner, bullets_in_magazine=12):
        super().__init__(owner, scene_image='other.gun', interface_image='interface.weapon_icons.Pistol',
                         bullets_in_magazine=bullets_in_magazine, magazine_size=12,
                         main_attack_interval=7, reload_time=40, ammo_type='Pistol',
                         accuracy=42, damage=60)


class BurstFiringPistol(RangedWeapon):
    """
    Стреляющий очередями пистолет
    """

    def __init__(self, owner, bullets_in_magazine=20):
        super().__init__(owner, scene_image='other.gun', interface_image='interface.weapon_icons.TwoBarrelShotgun',
                         bullets_in_magazine=bullets_in_magazine, magazine_size=20,
                         main_attack_interval=14, reload_time=60, ammo_type='Pistol',
                         accuracy=40, damage=60, combo_attack_interval=3, combo_size=4)


class Shotgun(RangedWeapon):
    """
    Дробовик
    """

    def __init__(self, owner, bullets_in_magazine=6):
        super().__init__(owner, scene_image='other.gun', interface_image='other.gun',
                         bullets_in_magazine=bullets_in_magazine, magazine_size=6,
                         main_attack_interval=12, reload_time=70, ammo_type='Shotgun',
                         accuracy=35, damage=50, shells=5)


class TwoBarrelShotgun(RangedWeapon):
    """
    Двустволка
    """

    def __init__(self, owner, bullets_in_magazine=2):
        super().__init__(owner, scene_image='other.gun', interface_image='interface.weapon_icons.TwoBarrelShotgun',
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

    def __init__(self, owner, bullets_in_magazine=3):
        super().__init__(owner, bullets_in_magazine)
        self.image_name = 'other.gun'
        self.interface_image = 'other.gun'
        self.magazine_size = 3
        self.alternative_attack_combo = 3


class TacticalShotgun(RangedWeapon):
    """
    Тактический дробоаик
    """

    def __init__(self, owner, bullets_in_magazine=6):
        super().__init__(owner, scene_image='other.gun', interface_image='other.gun',
                         bullets_in_magazine=bullets_in_magazine, magazine_size=6,
                         main_attack_interval=9, reload_time=70, ammo_type='Shotgun',
                         accuracy=42, damage=45, is_automatic=True, shells=4)


class AutomaticRifle(RangedWeapon):
    """
    Автоматическая винтовка
    """

    def __init__(self, owner, bullets_in_magazine=25):
        super().__init__(owner, scene_image='other.gun', interface_image='other.gun',
                         bullets_in_magazine=bullets_in_magazine, magazine_size=25,
                         main_attack_interval=4, reload_time=60, ammo_type='Rifle',
                         accuracy=60, damage=90, is_automatic=True)


class SniperRifle(RangedWeapon):
    """
    Снайперская винтовка
    """

    def __init__(self, owner, bullets_in_magazine=5):
        super().__init__(owner, scene_image='other.gun', interface_image='other.gun',
                         bullets_in_magazine=bullets_in_magazine, magazine_size=5,
                         main_attack_interval=20, reload_time=80, ammo_type='Rifle',
                         accuracy=110, damage=120)


class OldRifle(RangedWeapon):
    """
    Старая винтовка
    """

    def __init__(self, owner, bullets_in_magazine=8):
        super().__init__(owner, scene_image='other.gun', interface_image='other.gun',
                         bullets_in_magazine=bullets_in_magazine, magazine_size=8,
                         main_attack_interval=14, reload_time=40, ammo_type='Rifle',
                         accuracy=90, damage=90)


class SemiAutomaticRifle(OldRifle):
    """
    Полуавтоматическая винтовка
    """

    def __init__(self, owner, bullets_in_magazine=8):
        super().__init__(owner, bullets_in_magazine)
        self.image_name = 'other.gun'
        self.scene_image = 'other.gun'
        self.main_attack_interval = 10
        self.reload_time = 50
        self.accuracy = 60


class Sword(MeleeWeapon):

    def __init__(self, owner):
        super().__init__(owner, scene_image='other.gun', interface_image='other.gun',
                         main_attack_interval=15, length=60)


WEAPON_VOCABULARY = {
    'Pistol': Pistol,
    'BurstFiringPistol': BurstFiringPistol,
    'Shotgun': Shotgun,
    'TwoBarrelShotgun': TwoBarrelShotgun,
    'ThreeBarrelShotgun': ThreeBarrelShotgun,
    'TacticalShotgun': TacticalShotgun,
    'AutomaticRifle': AutomaticRifle,
    'SniperRifle': SniperRifle,
    'OldRifle': OldRifle,
    'SemiAutomaticRifle': SemiAutomaticRifle,
    'Sword': Sword,
}
