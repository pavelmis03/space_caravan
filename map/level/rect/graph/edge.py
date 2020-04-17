from typing import List, Tuple, Dict

DIRECTION = [0, 1, -1]

class Edge:
    """
    Ребро - возможный проход между прямоугольниками
    """
    def __init__(self, new1: Dict[str, int], new2: Dict[str, int], direction: List[int], arr):
        self.new1 = new1
        self.new2 = new2
        self.direction = direction
        self.color = [arr[new1['i']][new1['j']], arr[new2['i']][new2['j']]]
    def delete(self, arr: List[List[int]]):
        '''
        Присваивает двум стенам, разделяющим фигуры,
        какой-то цвет этих фигур.
        '''
        i = [self.new1['i'], self.new2['i']]
        j = [self.new1['j'], self.new2['j']]

        '''
        Стена лежит между i[0]j[0] и i[1]j[1]
        '''
        wall_i = i[0] + (i[1] - i[0]) // 2
        wall_j = j[0] + (j[1] - j[0]) // 2

        arr[wall_i][wall_j] = self.color[0]
        arr[wall_i + self.direction[0]][wall_j + self.direction[1]] = self.color[0]
        arr[wall_i - self.direction[0]][wall_j - self.direction[1]] = self.color[0]

class EdgeManager:
    """
    Ребро - три соседние связи с одинаковым смещением.
    Связь (connection) - две клетки различных цветов (не 0).

    Две клетки составляют связь, если существует стена, по 1 сторону (либо по оси x, либо по оси у)
    от нее первая клетка, а по другую (по той же оси) вторая.
    Клетки 1 и 2 не связь:
    144
    000
    332
    Пример ребра:
    102
    102
    102

    Этот огромный код необходим, чтобы можно было
    делать проходы в 3 клетки
    """
    def __init__(self, arr, used):
        self.arr = arr
        self.used = used
        self.connect_manager = ConnectManager(arr, used)

    def create_edge(self, connects: List[List[Dict[str, int]]],
                    direction: List[int], res: List[Edge]):
        """
        :param connects: список связей. connects[0] - список клеток одного прямоугольника, connects[1] - другого
        :param direction: направление, по которому расположены клетки
        :param res: куда нужно записать ответ
        """
        for i in range(len(connects)):
            for j in range(len(connects[i])):
                c = connects[i][j]
                self.used[c['i']][c['j']] = True

        res.append(Edge(connects[0][0], connects[1][0], direction, self.arr))

    def can_create_edge(self, connects: List[List[Dict[str, int]]]) -> bool:
        """
        Может ли создать ребро из этих связей

        цвета у связей должны быть равны соответственно
        :param connects: список связей. connects[0] - список клеток одного прямоугольника, connects[1] - другого
        """
        for i in range(len(connects)):
            for j in range(1, len(connects[i])):
                c1 = connects[i][j]
                c2 = connects[i][j - 1]

                if self.arr[c1['i']][c1['j']] != self.arr[c2['i']][c2['j']]:
                    return False
        return True

    def try_create_connects(self, i: int, j: int, dy: int, dx: int,
                            res: List[List[Dict[str, int]]]) -> bool:
        """
        Пробуем создать связь от клетки (i, j)

        Заполняет список res. В res[0] - клетки одного прямоугольника, в res[1] - другого.

        Сначала выбираем одну связь.

        всегда есть две связи, дополняющие эту связь до ребра
        например, если у нас есть горизонтальная связь
        102, то следующая может быть над ней (с меньшей i)
        или под ней (с большей i).
        Перебрать их можно, прибавляя к полученным координатам
        +dx[k], +dy[k] и -dx[k], -dy[k].

        (у основной связи direction == 0)
        """
        direction = DIRECTION
        for r in range(len(direction)):
            shift_i = direction[r] * dx
            shift_j = direction[r] * dy
            next1, next2 = \
                self.connect_manager.get_connect(i + shift_i, j + shift_j,
                                             dy, dx)
            if not self.connect_manager.can_connect(next1, next2):
                return False
            res[0].append(next1)
            res[1].append(next2)

        return True

class ConnectManager:
    """
    Менеджер связей
    """
    def __init__(self, arr, used):
        self.arr = arr
        self.used = used

    def get_connect(self, i: int, j: int, dy: int, dx: int) -> Tuple[Dict[str, int], Dict[str, int]]:
        """
        получить связь по клетке и смещению
        """
        new1 = self.get_shifted_coord(i, j, dy, dx)
        new2 = self.get_shifted_coord(i, j, -dy, -dx)
        return new1, new2

    def can_connect(self, new1: Dict[str, int], new2: Dict[str, int]) -> bool:
        """
        может ли создать связь

        связь можно сформировать, только между клетками различных фигур.
        Чтобы не рассматривать много случаев, уже использованные клетки не используются.
        """
        if self.used[new1['i']][new1['j']] or self.used[new2['i']][new2['j']]:
            return False

        return (self.arr[new1['i']][new1['j']] and self.arr[new2['i']][new2['j']] and
                        self.arr[new1['i']][new1['j']] != self.arr[new2['i']][new2['j']])

    def get_shifted_coord(self, i: int, j: int, dy: int, dx: int) -> Dict[str, int]:
        """
        получить клетку (i + dy, j + dx)
        """
        new_i = i + dy
        new_j = j + dx
        return {'i': new_i, 'j': new_j}
