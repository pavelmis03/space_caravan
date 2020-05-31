"""
Файл содержит словарь названий классов, которые могут сохраняться и подгружаться из списка с помощью процедур из
game_data_manager.py. Так можно загрузить список объектов разных классов вперемешку.
"""

from drawable_objects.ladder import Ladder
from drawable_objects.planet import Planet
from drawable_objects.space_map_terminal import SpaceMapTerminal
from drawable_objects.clone_capsule import CloneCapsule
from drawable_objects.enemy import Enemy
from map.level.rect.splitter import GridRectangle

CLASSES_BASE = {
    'Ladder': Ladder,
    'Planet': Planet,
    'SpaceMapTerminal': SpaceMapTerminal,
    'CloneCapsule': CloneCapsule,
    'Enemy': Enemy,
    # для сохранения оптимизированной структуры grid_interaction_with_enemy
    'GridRectangle': GridRectangle
}
