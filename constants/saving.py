from drawable_objects.ladder import Ladder
from drawable_objects.planet import Planet
from drawable_objects.space_map_terminal import SpaceMapTerminal
from drawable_objects.enemy import Enemy
from map.level.rect.splitter import GridRectangle

CLASSES_BASE = {
    'Ladder': Ladder,
    'Planet': Planet,
    'SpaceMapTerminal': SpaceMapTerminal,
    'Enemy': Enemy,
    # для сохранения оптимизированной структуры grid_interaction_with_enemy
    'GridRectangle': GridRectangle
}
