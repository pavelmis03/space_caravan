from map.level.rect.graph_manager import RectGraphManager
from utils.disjoint_set import DisjointSet
from utils.random import is_random_proc, shuffle


class RectConnecter:
    def __init__(self, arr, is_vertex_of_rect, rects_count):
        self.arr = arr

        self.edges = []
        RectGraphManager.save_edges_between_rects(self.arr,
                            is_vertex_of_rect, self.edges)

        self.rects_count = rects_count

    def start_random_connection(self):
        """
        делает проходы(двери) между прямоугольниками.

        :return:
        """
        shuffle(self.edges)
        self.dis_set = DisjointSet(self.rects_count)
        for i in range(len(self.edges)):
            edge = self.edges[i]
            if not self.dis_set.check(edge.color[0], edge.color[1]):
                self.dis_set.union(edge.color[0], edge.color[1])
                edge.delete(self.arr)
                continue

            CHANCE_EXTRA_CONNECTION = 1
            if is_random_proc(CHANCE_EXTRA_CONNECTION):
                edge.delete(self.arr)