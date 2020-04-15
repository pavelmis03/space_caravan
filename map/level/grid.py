from drawable_objects.enemy import Enemy
from enemy_interaction_with_grid.manager import GridInteractionWithEnemyManager
from geometry.point import Point
from map.collision_grid.collision_grid import CollisionGrid
from map.level.generator import LevelGenerator, EnemyGenerator


class LevelGrid(CollisionGrid):
    """
    Сетка уровня (данжа).
    """
    def _create_interaction_with_enemy_manager(self):
        """
        Необходимо вызывать до enemy_generation.

        InteractionWithEnemyManager использует информацию из LevelGenerator
        (Он создает прямоугольники коллизий на основе комнат)
        """
        self.enemy_interaction_manager = GridInteractionWithEnemyManager(
            self._room_rectangles, self._arr_after_split, self)

        # удаляем ненужные переменные, чтобы освободить память:
        del self._arr_after_split
        del self._room_rectangles

    def enemy_generation(self):
        """
        Генерация врагов с помощью EnemyGenerator
        """
        self._create_interaction_with_enemy_manager()

        enemy_generator = EnemyGenerator(self)
        enemy_generator.generate()

    def map_construction(self, min_area: int = 100, min_w: int = 8, min_h: int = 8):
        """
        Генерация уровня с помощью LevelGenerator
        """
        generator = LevelGenerator(self.arr, min_area, min_w, min_h)
        generator.generate()

        self._room_rectangles = generator.rect_splitter.rectangles
        self._arr_after_split = generator.arr_after_split

    def process_logic(self):
        self.enemy_interaction_manager.process_logic()

    def is_enemy_see_player(self, enemy: Enemy) -> bool:
        return self.enemy_interaction_manager.is_enemy_see_player(enemy)

    def get_pos_to_move(self, enemy: Enemy) -> Point:
        return self.enemy_interaction_manager.get_pos_to_move(enemy)
