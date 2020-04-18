from math import ceil
from typing import Tuple, List, Set, Dict


from enemy_interaction_with_grid.hearing.manager import EnemyHearingManager
from drawable_objects.enemy import Enemy
from geometry.point import Point
from geometry.segment import Segment
from geometry.rectangle import Rectangle
from geometry.vector import cross_product, sign
from geometry.distances import dist
from geometry.intersections import intersect_segments
from utils.list import is_indexes_correct


class SynopticOccasion:
    def __init__(self, relative_pos: Point, synoptic_segments: List[Segment], visible: Set[int]):
        self._pos = relative_pos
        self.__semiplane = self.__get_semiplane(self._pos)
        self._synoptic_segments = synoptic_segments
        self._visible = visible

    def execute(self):
        pass

    def idle_execute(self):
        pass

    def __get_semiplane(self, pos: Point) -> int:
        if sign(pos.y) == 0:
            if pos.x > 0:
                return 0
            else:
                return 1
        if pos.y < 0:
            return 0
        else:
            return 1

    def __lt__(self, other):
        if self.__semiplane != other.__semiplane:
            return self.__semiplane < other.__semiplane
        return cross_product(self._pos, other._pos) < 0


class OccasionChangeState(SynopticOccasion):
    def __init__(self, relative_pos: Point, synoptic_segments: List[Segment], visible: Set[int],
                 segment_index: int):
        super().__init__(relative_pos, synoptic_segments, visible)
        self._segment_index = segment_index

    def idle_execute(self):
        self.execute()


class OccasionBegin(OccasionChangeState):
    def execute(self):
        self._visible.add(self._segment_index)


class OccasionEnd(OccasionChangeState):
    def execute(self):
        if self._segment_index in self._visible:
            self._visible.remove(self._segment_index)


class OccasionQuery(SynopticOccasion):
    def __init__(self, relative_pos: Point, synoptic_segments: List[Segment], visible: Set[int],
                 enemy: Enemy, answer: Dict[Enemy, int]):
        super().__init__(relative_pos, synoptic_segments, visible)
        self.__enemy = enemy
        self.__answer = answer

    def execute(self):
        vision_segment = Segment(Point(0, 0), self._pos)
        for index in self._visible:
            if intersect_segments(vision_segment, self._synoptic_segments[index]):
                self.__answer[self.__enemy] = False
                return
        self.__answer[self.__enemy] = True


class EnemyVisionWizard:
    VISION_RADIUS = Enemy.VISION_RADIUS

    def __init__(self, grid, hearing_manager: EnemyHearingManager):
        self.__grid = grid
        self.__hearing_manager = hearing_manager
        self.__scene = self.__grid.scene
        self.__enemies = self.__scene.enemies
        self.__player = self.__scene.player

        self.__index_range = int(ceil(EnemyVisionWizard.VISION_RADIUS / self.__grid.cell_width))
        self.__cell_used = [[] for _ in range(2 * self.__index_range + 1)]
        for i in range(2 * self.__index_range + 1):
            self.__cell_used[i] = [False for _ in range(2 * self.__index_range + 1)]

        self.__answer = {}

    def __unite_rects(self, rect1: Rectangle, rect2: Rectangle) -> Rectangle:
        result_left = min(rect1.left, rect2.left)
        result_right = max(rect1.right, rect2.right)
        result_top = min(rect1.top, rect2.top)
        result_bottom = max(rect1.bottom, rect2.bottom)
        return Rectangle(result_left, result_top, result_right, result_bottom)

    def __get_cell_used(self, i: int, j: int) -> bool:
        if not is_indexes_correct(self.__cell_used, i + self.__index_range, j + self.__index_range):
            return True
        return self.__cell_used[i + self.__index_range][j + self.__index_range]

    def __set_cell_used(self, i: int, j: int, new_value: bool):
        self.__cell_used[i + self.__index_range][j + self.__index_range] = new_value

    def __get_wall_rect(self, i: int, j: int, player_index: Tuple[int, int]) -> Rectangle:
        if self.__get_cell_used(i, j):
            return None
        self.__set_cell_used(i, j, True)
        absolute_i = player_index[0] + i
        absolute_j = player_index[1] + j
        if not is_indexes_correct(self.__grid.arr, absolute_i, absolute_j):
            return None
        if self.__grid.is_passable(absolute_i, absolute_j):
            return None
        return self.__grid.get_collision_rect(absolute_i, absolute_j)

    def __make_long_rect(self, i: int, j: int, dir: Tuple[int, int], player_index: Tuple[int, int]) -> Rectangle:
        result_rect = self.__get_wall_rect(i, j, player_index)
        if not result_rect:
            return None
        while True:
            i += dir[0]
            j += dir[1]
            next_rect = self.__get_wall_rect(i, j, player_index)
            if not next_rect:
                break
            result_rect = self.__unite_rects(result_rect, next_rect)
        return result_rect


    def __get_united_rects(self) -> List[Rectangle]:
        walls_rects = []
        player_index = self.__grid.get_index_by_pos(self.__player.pos)
        for i in range(-self.__index_range, self.__index_range + 1):
            for j in range(-self.__index_range, self.__index_range + 1):
                self.__set_cell_used(i, j, False)

        for i in range(-self.__index_range, self.__index_range + 1):
            for j in range(-self.__index_range, self.__index_range + 1):
                wall_rect = self.__get_wall_rect(i, j, player_index)
                if not wall_rect:
                    continue
                long_rect = self.__make_long_rect(i, j + 1, [0, 1], player_index)
                if not long_rect:
                    long_rect = self.__make_long_rect(i + 1, j, [1, 0], player_index)
                if long_rect:
                    wall_rect = self.__unite_rects(wall_rect, long_rect)
                walls_rects.append(wall_rect)

        return walls_rects

    def __get_synoptic_segment(self, rect: Rectangle) -> Segment:
        rect_vertexes = rect.get_vertexes()
        left_point = right_point = rect_vertexes[0]
        for vertex in rect_vertexes:
            vector_to_vertex = vertex - self.__player.pos
            if cross_product(left_point - self.__player.pos, vector_to_vertex) > 0:
                left_point = vertex
            if cross_product(right_point - self.__player.pos, vector_to_vertex) < 0:
                right_point = vertex
        return Segment(left_point - self.__player.pos, right_point - self.__player.pos)

    def __get_occasions(self, synoptic_segments: List[Segment]) -> List[SynopticOccasion]:
        occasions = []
        visible = set()
        for i in range(len(synoptic_segments)):
            occasions.append(OccasionBegin(synoptic_segments[i].p1, synoptic_segments, visible, i))
            occasions.append(OccasionEnd(synoptic_segments[i].p2, synoptic_segments, visible, i))
        for enemy in self.__enemies:
            if dist(self.__player.pos, enemy.pos) <= EnemyVisionWizard.VISION_RADIUS:
                occasions.append(OccasionQuery(enemy.pos - self.__player.pos, synoptic_segments, visible, enemy, self.__answer))
            else:
                self.__answer[enemy] = False
        occasions.sort()
        return occasions

    def __run_occasions(self, occasions: List[SynopticOccasion]):
        for oc in occasions:
            oc.idle_execute()
        for oc in occasions:
            oc.execute()

    def process_logic(self):
        self.__answer.clear()
        walls_rects = self.__get_united_rects()
        synoptic_segments = []
        for i in range(len(walls_rects)):
            synoptic_segments.append(self.__get_synoptic_segment(walls_rects[i]))
        occasions = self.__get_occasions(synoptic_segments)
        self.__run_occasions(occasions)

    def enemy_sees_player(self, enemy: Enemy) -> bool:
        return self.__answer[enemy]