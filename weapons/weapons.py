from weapons.base import RangedWeapon


class Pistol(RangedWeapon):
    """
    Пистолет
    """
    def __init__(self, owner, ammo, bullets_in_magazine=12):
        super().__init__(owner, ammo, bullets_in_magazine, magazine_size=12,
                         main_attack_interval=9, reload_time=40, bullet_type='Pistol',
                         accuracy=80)


class Shotgun(RangedWeapon):
    """
    Дробовик
    """
    def __init__(self, owner, ammo, bullets_in_magazine=6):
        super().__init__(owner, ammo, bullets_in_magazine, magazine_size=6,
                         main_attack_interval=15, reload_time=80, bullet_type='Shotgun',
                         accuracy=35, shells=5)


class BurstFiringPistol(RangedWeapon):
    """
    Типо пистолет, но стрляет очередями и прикольнаааааа
    """
    def __init__(self, owner, ammo, bullets_in_magazine=20):
        super().__init__(owner, ammo, bullets_in_magazine, magazine_size=20,
                         main_attack_interval=15, reload_time=60, bullet_type='Pistol',
                         accuracy=40, combo_attack_interval=3, combo_size=4)


class AutomaticRifle(RangedWeapon):
    """
    Автоматическая винтовка
    """
    def __init__(self, owner, ammo, bullets_in_magazine=25):
        super().__init__(owner, ammo, bullets_in_magazine, magazine_size=25,
                         main_attack_interval=4, reload_time=60, bullet_type='Rifle',
                         accuracy=65, is_automatic=True)
