from drawable_objects.player import Player #не удалять. без этой строчки все ломается
from drawable_objects.ladder import Ladder
from drawable_objects.planet import Planet
from drawable_objects.space_map_terminal import SpaceMapTerminal
from drawable_objects.enemy import Enemy
from map.level.rect.splitter import GridRectangle
from drawable_objects.chest import Chest
from drawable_objects.drop.chest_drop import WeaponDrop



CLASSES_BASE = {
    'Ladder': Ladder,
    'Planet': Planet,
    'SpaceMapTerminal': SpaceMapTerminal,
    'Enemy': Enemy,
    # для сохранения оптимизированной структуры grid_interaction_with_enemy
    'GridRectangle': GridRectangle,
    'WeaponDrop': WeaponDrop,
    'Chest': Chest
}
