from typing import Dict

from utils.sound import SoundManager
from weapons.base import Weapon, RangedWeapon, MeleeWeapon


class Pistol(RangedWeapon):
    """
    Пистолет
    """
    IMAGE_NAME = 'weapons.pistol'
    SHOOT_SOUND = 'weapon.attack.pistol'
    RELOAD_SOUND = 'weapon.reload.pistol'
    DESCRIPTION = """
                Оружие: Пистолет
                Тип: Средние дистанции
                Урон: 45
                Точность: 42
                Интервал стрельбы: 9
                Время перезарядки: 40
                Ваше первоначальное оружие
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
    SHOOT_SOUND = 'weapon.attack.pistol'
    RELOAD_SOUND = 'weapon.reload.pistol'
    DESCRIPTION = """
                    Оружие: Пистолет стреляющий очередями
                    Тип: Средние дистанции
                    Урон: 35
                    Точность: 40
                    Интервал между очередями: 14
                    Время перезарядки: 40
                    Очереди стреляющие пистолетом. Стоп, что-то тут не так... 
                    """

    def __init__(self, owner, bullets_in_magazine=20):
        super().__init__(owner, interface_image='interface.weapon_icons.burst_firing_pistol',
                         bullets_in_magazine=bullets_in_magazine, magazine_size=20,
                         main_attack_interval=14, reload_time=40, ammo_type='Pistol',
                         accuracy=40, damage=35, combo_attack_interval=3, combo_size=4)


class Shotgun(RangedWeapon):
    """
    Дробовик
    """
    IMAGE_NAME = 'weapons.shotgun'
    SHOOT_SOUND = 'weapon.attack.shotgun'
    RELOAD_SOUND = 'weapon.reload.shotgun'
    DESCRIPTION = """
                   Оружие: Дробовик
                   Тип: Средние дистанции
                   Урон: 50
                   Точность: 33
                   Интервал стрельбы: 15
                   Время перезарядки: 70
                   Ну тут все просто, стреляй по толпе и хоть в кого-то точно попадешь 
                   """

    def __init__(self, owner, bullets_in_magazine=6):
        super().__init__(owner, interface_image='interface.weapon_icons.shotgun',
                         bullets_in_magazine=bullets_in_magazine, magazine_size=6,
                         main_attack_interval=15, reload_time=70, ammo_type='Shotgun',
                         accuracy=33, damage=50, shells=5)


class TwoBarrelShotgun(RangedWeapon):
    """
    Двустволка
    """
    IMAGE_NAME = 'weapons.two_barrel_shotgun'
    SHOOT_SOUND = 'weapon.attack.shotgun'
    RELOAD_SOUND = 'weapon.reload.shotgun'
    DESCRIPTION = """
                    Оружие: Двустволка
                    Тип: Дальние дистанции
                    Урон: 35
                    Точность: 32
                    Интервал стрельбы: 8
                    Время перезарядки: 35
                    Два ствола всегда лучше чем один
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
    SHOOT_SOUND = 'weapon.attack.shotgun'
    RELOAD_SOUND = 'weapon.reload.shotgun'
    DESCRIPTION = """
                    Оружие: Трёхстволка
                    Тип: Средние дистанции
                    Урон: 35
                    Точность: 32
                    Интервал стрельбы: 8
                    Время перезарядки: 40
                    Ты прикинь! Мы смогли приделать к твоей волыне еще один ствол!
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
    SHOOT_SOUND = 'weapon.attack.shotgun'
    RELOAD_SOUND = 'weapon.reload.shotgun'
    DESCRIPTION = """
                    Оружие: Тактический дробовик
                    Тип: Средние дистанции
                    Урон: 45
                    Точность: 40
                    Интервал стрельбы: 9
                    Время перезарядки: 70
                    С самого начала у этого дробовика была какая-то тактика
                    и он ее придерживался
                    """

    def __init__(self, owner, bullets_in_magazine=6):
        super().__init__(owner, interface_image='interface.weapon_icons.tactical_shotgun',
                         bullets_in_magazine=bullets_in_magazine, magazine_size=6,
                         main_attack_interval=9, reload_time=70, ammo_type='Shotgun',
                         accuracy=40, damage=45, is_automatic=True, shells=4)


class AutomaticRifle(RangedWeapon):
    """
    Автоматическая винтовка
    """
    IMAGE_NAME = 'weapons.automatic_rifle'
    SHOOT_SOUND = 'weapon.attack.rifle2'
    RELOAD_SOUND = 'weapon.reload.rifle2'
    DESCRIPTION = """
                Оружие: Автоматическая винтовка
                Тип: Средние дистанции
                Урон: 30
                Точность: 40
                Интервал стрельбы: 2
                Время перезарядки: 60
                Эта винтовка настолько автоматическая, что ты ей, впрочем, и не нужен...
                """

    def __init__(self, owner, bullets_in_magazine=30):
        super().__init__(owner, interface_image='interface.weapon_icons.automatic_rifle',
                         bullets_in_magazine=bullets_in_magazine, magazine_size=30,
                         main_attack_interval=2, reload_time=60, ammo_type='Rifle',
                         accuracy=40, damage=45, is_automatic=True)


class SniperRifle(RangedWeapon):
    """
    Снайперская винтовка
    """
    IMAGE_NAME = 'weapons.sniper_rifle'
    SHOOT_SOUND = 'weapon.attack.rifle1'
    RELOAD_SOUND = 'weapon.reload.rifle1'
    DESCRIPTION = """
                Оружие: Снайперская винтовка
                Тип: Дальние дистанции
                Урон: 120
                Точность: 110
                Интервал стрельбы: 25
                Время перезарядки: 100
                Она настолько крутая, что с ее помощью ты сможешь попасть в глаз на расстоянии 300 м, правда себе...  
                """

    def __init__(self, owner, bullets_in_magazine=5):
        super().__init__(owner, interface_image='interface.weapon_icons.sniper_rifle',
                         bullets_in_magazine=bullets_in_magazine, magazine_size=5,
                         main_attack_interval=25, reload_time=100, ammo_type='Rifle',
                         accuracy=110, damage=120)


class OldRifle(RangedWeapon):
    """
    Старая винтовка
    """
    IMAGE_NAME = 'weapons.old_rifle'
    SHOOT_SOUND = 'weapon.attack.rifle2'
    RELOAD_SOUND = 'weapon.reload.rifle2'
    DESCRIPTION = """
                        Оружие: Довоенная винтовка
                        Тип: Дальние дистанции
                        Урон: 80
                        Точность: 80
                        Интервал стрельбы: 15
                        Время перезарядки: 50
                        Винтовка твоего деда, из нее он стрелял еще по фашистам с Альфа Центавры  
                        """


    def __init__(self, owner, bullets_in_magazine=8):
        super().__init__(owner, interface_image='interface.weapon_icons.old_rifle',
                         bullets_in_magazine=bullets_in_magazine, magazine_size=8,
                         main_attack_interval=15, reload_time=50, ammo_type='Rifle',
                         accuracy=80, damage=80)


class SemiAutomaticRifle(RangedWeapon):
    """
    Полуавтоматическая винтовка
    """
    IMAGE_NAME = 'weapons.semi_automatic_rifle'
    SHOOT_SOUND = 'weapon.attack.rifle1'
    RELOAD_SOUND = 'weapon.reload.rifle1'
    DESCRIPTION = """
                        Оружие: Полуавтоматическая винтовка
                        Тип: Дальние дистанции
                        Урон: 80
                        Точность: 60
                        Интервал стрельбы: 10
                        Время перезарядки: 50
                        Почти как автоматическая винтовка, только наполовину  
                        """

    def __init__(self, owner, bullets_in_magazine=8):
        super().__init__(owner, interface_image='interface.weapon_icons.semi_automatic_rifle',
                         bullets_in_magazine=bullets_in_magazine, magazine_size=8,
                         main_attack_interval=9, reload_time=50, ammo_type='Rifle',
                         accuracy=60, damage=80)


class Sword(MeleeWeapon):
    """
    Меч
    """
    IMAGE_NAME = 'other.gun'
    ATTACK_SOUND = 'weapon.attack.sword'
    DESCRIPTION = """
                            Оружие: Меч
                            Тип: Ближние дистанции
                            Урон: 999
                            Точность: 999
                            Интервал удара: 15
                            Время перезарядки: ОНА ЕМУ НЕ НУЖНА
                            Зачем воину меч, если он не в крови?
                            """

    def __init__(self, owner):
        super().__init__(owner, interface_image='other.gun',
                         main_attack_interval=15, length=60)


class Knife(MeleeWeapon):
    """
    Нож(только для Player)
    """
    IMAGE_NAME = 'weapons.knife'
    ANIMATION = [
        'moving_objects.player.knife1',
        'moving_objects.player.knife2',
    ]
    ATTACK_SOUND = 'weapon.attack.sword'
    DESCRIPTION = """
                            Оружие: Меч
                            Тип: Ближние дистанции
                            Урон: 999
                            Точность: 999
                            Интервал удара: 15
                            Время перезарядки: ОНА ЕМУ НЕ НУЖНА
                            Этим ножом можно резать масло как своих врагов
                            """

    def __init__(self, owner):
        super().__init__(owner, interface_image='interface.weapon_icons.knife',
                         main_attack_interval=15, length=60)
        self.one_animation_frame_vision_time = 3
        self.animation_ind = -1

    def attack(self):
        super().attack()
        self.scene.player.image_name = self.ANIMATION[0]
        self.animation_ind = 0

    def process_logic(self):
        if self.animation_ind != -1:
            if self.animation_ind == (self.one_animation_frame_vision_time * len(self.ANIMATION)):
                self.animation_ind = -1
                self.scene.player.image_name = 'moving_objects.player.knife'
            else:
                self.scene.player.image_name = self.ANIMATION[self.animation_ind //
                                                              self.one_animation_frame_vision_time]
                self.animation_ind += 1
        super().process_logic()


class Fist(MeleeWeapon):
    """
    Кулак(персонаж бьёт только одним)
    """
    ATTACK_SOUND = 'weapon.attack.fist'
    DESCRIPTION = """
                                Оружие: братиш, у тебя его нет
                                Тип: а да
                                Урон: 25
                                Точность: ну так себе
                                Интервал удара: 8
                                Время перезарядки: ручки быстро устают
                                Ты конечно можешь подкрасться к роботу сзади и открутить роботу голову, 
                                но идти в бой без оружия может только безмозглый или Чак Норрис, 
                                но что-то я не вижу на тебе шляпы
                                """

    def __init__(self, owner):
        super().__init__(owner, interface_image='interface.weapon_icons.nothing',
                         main_attack_interval=8, length=40)

    def attack(self):
        """
        Функция атаки
        """
        from drawable_objects.slash import Punch
        SoundManager.play_sound(self.ATTACK_SOUND)
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
    'Knife': Knife,
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
    'Knife': 'weapons_on_floor.knife',
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
