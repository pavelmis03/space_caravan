from typing import List

from map.level.rect.graph.manager import RectGraphManager

from map.level.rect.splitter import RectSplitter
from map.level.rect.unioner import RectUnioner
from map.level.rect.connecter import RectConnecter


class LevelGenerator:
    """
    Принимает arr. Далее заполняет его числами.
    Если ноль, то стена. Иначе пол.
    Разные числа означают границы разных фигур.

    Результат генерации - заполнение исходного прямоугольника фигурами
    с углами 270 и 90 градусов.
    """
    def __init__(self, arr:List[List[int]],
                 min_area: int=100, min_w: int=8, min_h: int=8):
        self.arr = arr

        self.rect_splitter = RectSplitter(self.arr, min_area, min_w, min_h)

    def generate(self):
        """
        Прямоугольник разбивается на много прямоугольников.

        Далее некоторые из них объединяются (для получения фигур помимо прямоугольников).

        После проводятся ребра (двери) между полученными фигурами.

        Граф связный, но не обязательно является деревом.
        """
        self.split()

        self.union()

        self.connect()

    def split(self):
        self.rect_splitter.start_random_split()
        self.graph_manager = RectGraphManager(self.rect_splitter.arr, self.rect_splitter.rects_count)

    def union(self):
        self.rect_unioner = RectUnioner(self.graph_manager)
        self.rect_unioner.start_random_union()
        self.rect_unioner.delete_edges()

    def connect(self):
        self.rect_connecter = RectConnecter(self.graph_manager)
        self.rect_connecter.start_random_connection()