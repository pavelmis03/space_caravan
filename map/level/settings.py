from typing import List, Tuple


class LevelSettings:
    def __init__(self, floor_img: str, wall_img: str, enemy_weapons: List[Tuple[int, str]]):
        """
        :param floor_img: картинка пола (строка)
        :param wall_img: картинка стены (строка)
        :param enemy_weapons: список оружий, доступных Enemy ([вероятность, название оружия]).
        сумма вероятностей должны быть равна 100.
        """
        self.level_filenames = [wall_img, floor_img] #порядок важен

        self.enemy_weapons = enemy_weapons
        sum_chance = 0
        for item in self.enemy_weapons:
            sum_chance += item[0]
        if sum_chance != 100:
            raise Exception('sum of enemy_weapons chance not equal 100. The value: {}'.format(sum_chance))


# список настроек для каждого уровня.
level_settings = [
    LevelSettings('level.floor3', 'level.wall1',
                [(30, 'Sword'), (60, 'Pistol'), (10, 'TwoBarrelShotgun')]),
    LevelSettings('level.floor3', 'level.wall1',
                [(30, 'Pistol'), (10, 'TwoBarrelShotgun'),
                 (30, 'OldRifle'), (30, 'SemiAutomaticRifle')]),
    LevelSettings('level.floor3', 'level.wall1',
                [(30, 'SemiAutomaticRifle'), (30, 'ThreeBarrelShotgun'),
                 (25, 'SniperRifle'), (15, 'BurstFiringPistol')]),
    LevelSettings('level.floor3', 'level.wall1',
                [(10, 'Sword'), (30, 'SniperRifle'), (30, 'Shotgun'), (30, 'AutomaticRifle')]),
    LevelSettings('level.floor3', 'level.wall1',
                [(10, 'Sword'), (20, 'AutomaticRifle'), (30, 'Shotgun'), (40, 'TacticalShotgun')])
]