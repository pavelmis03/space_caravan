from typing import Dict

from drawable_objects.ladder import Ladder
from drawable_objects.planet import Planet
from drawable_objects.space_map_terminal import SpaceMapTerminal
from drawable_objects.enemy import Enemy
from drawable_objects.base import DrawableObject


CLASSES_BASE = {
    'Ladder': Ladder,
    'Planet': Planet,
    'SpaceMapTerminal': SpaceMapTerminal,
    'Enemy': Enemy,
}
