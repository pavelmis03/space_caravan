from typing import List, Tuple
from utils.list import check_chance_list


class LevelSettings:
    CHEST_WEAPON_DROP_CHANCE = 40
    CHEST_OTHER_DROP = [(30, 'MedKit'), (30, 'Essence'), (40, 'Fuel')]
    def __init__(self, floor_img: str, wall_img: str,
                 enemy_weapons: List[Tuple[int, str]], chest_weapon_drop: List[Tuple[int, str]]):
        """
        :param floor_img: картинка пола (строка)
        :param wall_img: картинка стены (строка)
        :param enemy_weapons: список оружий, доступных Enemy ([вероятность, название оружия]).
        сумма вероятностей должны быть равна 100.
        :param chest_weapon_drop: список дропа ([вероятность, название дропа]).
        сумма вероятностей должна быть равна 100
        """
        self.level_filenames = [wall_img, floor_img] #порядок важен

        self.enemy_weapons = enemy_weapons
        self.chest_weapon_drop = chest_weapon_drop

        chance_lists = [self.enemy_weapons, self.chest_weapon_drop, self.CHEST_OTHER_DROP]
        for item in chance_lists:
            check_chance_list(item)


# список настроек для каждого уровня.
level_settings = [
    LevelSettings('level.floor3', 'level.wall1',
                [(30, 'Sword'), (60, 'Pistol'), (10, 'TwoBarrelShotgun')],
                  [(20, 'Sword'), (40, 'TwoBarrelShotgun'), (40, 'OldRifle')]),
    LevelSettings('level.floor3', 'level.wall1',
                [(30, 'Pistol'), (10, 'TwoBarrelShotgun'),
                 (30, 'OldRifle'), (30, 'SemiAutomaticRifle')],
                  [(40, 'SemiAutomaticRifle'), (40, 'ThreeBarrelShotgun'), (20, 'SniperRifle')]),
    LevelSettings('level.floor3', 'level.wall1',
                [(30, 'SemiAutomaticRifle'), (30, 'ThreeBarrelShotgun'),
                 (25, 'SniperRifle'), (15, 'BurstFiringPistol')],
                  [(16, 'SniperRifle'), (28, 'BurstFiringPistol'),
                   (28, 'Shotgun'), (28, 'AutomaticRifle')]),
    LevelSettings('level.floor3', 'level.wall1',
                [(10, 'Sword'), (30, 'SniperRifle'), (30, 'Shotgun'), (30, 'AutomaticRifle')],
                  [(30, 'Sword'), (50, 'AutomaticRifle'), (20, 'TacticalShotgun')]),
    LevelSettings('level.floor3', 'level.wall1',
                [(10, 'Sword'), (20, 'AutomaticRifle'), (30, 'Shotgun'), (40, 'TacticalShotgun')],
                  [(40, 'AutomaticRifle'), (60, 'TacticalShotgun')])
]
