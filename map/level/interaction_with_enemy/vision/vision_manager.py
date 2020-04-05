from drawable_objects.enemy import Enemy
from map.level.interaction_with_enemy.vision.vision_walls_intersection import VisionWallsIntersection


class EnemyVisionManager:
    """
    Vision распространяется только по сторонам квадрата.

    Обертка для VisionWallsIntersection

    Enemy видит Player если
    прямая, соединяющая клетку Player и клетку данного Enemy не
    пересекает стены (в действительности алгоритм неточен и
    работает немного по-другому, зато быстро. см. VisionWallsIntersection)
    """
    def __init__(self, grid):
        self.vision_walls_intersection = VisionWallsIntersection(grid)

    def is_enemy_see_player(self, enemy: Enemy) -> bool:
        """
        Может быть, нужно еще учитывать поворот Enemy.
        """
        return self.vision_walls_intersection.is_see_player(enemy)

    def process_logic(self):
        self.vision_walls_intersection.update_cant_see_to_enemies(Enemy.VISION_RANGE)