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

'''
= [
        ('level_objects.simple_planet', 0.07),
        ('level_objects.ice_planet', 0.35),
        ('level_objects.lava_planet', 0.3),
        ('level_objects.violet_planet', 0.3),
        ('level_objects.mushroom_planet', 0.3),
    ]
'''

# список настроек для каждого уровня.
level_settings = [
    LevelSettings('level.floor3', 'level.wall1',
                [(40, 'Pistol'), (30, 'Pistol'), (30, 'TwoBarrelShotgun')]), #первое должно быть Sword
    LevelSettings('level.floor3', 'level.wall1',
                [(40, 'Pistol'), (30, 'Pistol'), (30, 'TwoBarrelShotgun')]),
    LevelSettings('level.floor3', 'level.wall1',
                [(40, 'Pistol'), (30, 'Pistol'), (30, 'TwoBarrelShotgun')]),
    LevelSettings('level.floor3', 'level.wall1',
                [(40, 'Pistol'), (30, 'Pistol'), (30, 'TwoBarrelShotgun')]),
    LevelSettings('level.floor3', 'level.wall1',
                [(40, 'Pistol'), (30, 'Pistol'), (30, 'TwoBarrelShotgun')])
]