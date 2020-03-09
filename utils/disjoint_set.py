"""
Disjoint-set data structure = Система непересекающихся множеств (СНМ)
"""
class DisjointSet:
    """
    При возникновениии вопросов см e-maxx
    """
    def __init__(self, _length: int):
        self.parent = [i for i in range(_length)]
        self.height = [0 for i in range(_length)]
    def get_parent(self, a: int) -> int:
        if self.parent[a] == a:
            return a
        self.parent[a] = self.get_parent(self.parent[a])
        return self.parent[a]
    def check(self, a: int, b: int) -> bool:
        """
        true если а и b в одном множестве

        :param a:
        :param b:
        :return:
        """
        return self.get_parent(a) == self.get_parent(b)
    def union(self, a: int, b: int):
        p_a = self.get_parent(a)
        p_b = self.get_parent(b)

        if self.height[p_a] > self.height[p_b]:
            self.parent[p_b] = p_a
        elif self.height[p_a] < self.height[p_b]:
            self.parent[p_a] = p_b
        else:
            self.parent[p_a] = p_b
            self.height[p_b] += 1
