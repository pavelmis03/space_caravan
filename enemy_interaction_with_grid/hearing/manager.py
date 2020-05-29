from drawable_objects.enemy import Enemy
from enemy_interaction_with_grid.hearing.path_finder import GridPathFinder
from geometry.point import Point


class EnemyHearingManager:
    """
    Сейчас представляет собой обертку для path_finder

    Не доделано до конца.
    Enemy должен реагировать на выстрел игрока (или нет)
    """

    def __init__(self, grid):
        self.__path_finder = GridPathFinder(grid)

    def get_pos_to_move(self, enemy: Enemy) -> Point:
        """
        Получить точку для движения
        """
        return self.__path_finder.get_pos_to_move(enemy)

    def can_stay(self, i: int, j: int):
        """
        Может ли Enemy стоять на клетке с индексами i, j
        """
        return self.__path_finder.can_stay(i, j)

    def is_hearing_player(self, enemy: Enemy) -> bool:
        """
        Может ли услышать Enemy Player'а
        """
        return self.__path_finder.is_hearing_player(enemy)

    def save_enemy_pos(self, pos: Point):
        """
        отмечает, что на этой позиции есть enemy
        """
        self.__path_finder.save_enemy_pos(pos)

    def process_logic(self):
        """
        Логика менеджера
        """
        self.__path_finder.update_path_to_enemies(Enemy.HEARING_RANGE)
