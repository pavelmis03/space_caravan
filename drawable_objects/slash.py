from controller.controller import Controller
from drawable_objects.base import GameSprite
from geometry.circle import Circle
from geometry.intersections import intersect_seg_circle
from geometry.point import Point
from geometry.segment import Segment
from geometry.vector import vector_from_length_angle, length
from scenes.base import Scene
from utils.image import ImageManager


def dist(p1: Point, p2: Point) -> float:
    """
    Расстояние между точками.

    :param p1: первая точка
    :param p2: вторая точка
    :return: числовое значение, или 10^8, если одной из точек нет
    """
    if p1 is None or p2 is None:
        return 100000000
    return length(p2 - p1)


class Slash(GameSprite):
    """
    Базовый удар ближним оружием (далек от завершения).

    :param scene: сцена, на которой находится анимация удара
    :param controller: контроллер
    :param pos: начальная позиция удара
    :param angle: начальный угол направления удара
    """

    IMAGE_ZOOM = 0.4
    IMAGE_NAME = 'moving_objects.melee_weapon.attack.heavy_splash.1'

    def __init__(self, scene: Scene, controller: Controller, pos: Point, angle: float, damage):
        super().__init__(scene, controller, Slash.IMAGE_NAME, pos, angle, Slash.IMAGE_ZOOM)
        self.direction = vector_from_length_angle(10, self.angle)
        self.damage = damage
        ImageManager.process_draw(
            'moving_objects.melee_weapon.attack.heavy_splash.1', self.pos, self.scene.screen, 1, self.angle)
        self.scene.game_objects.append(Slash_Animation(self.scene, self.controller, self.pos, self.angle))
        self.destroy()

    def collision_manager(self, next_pos: Point):
        """
        Метод обработки всех возможных коллизий, нахождения близжайшей из них к pos удара
        и выполнения соответствующего виду коллизии метода

        """
        trajectory = Segment(self.pos, next_pos)

        intersect_walls_point = self.scene.grid.intersect_seg_walls(trajectory)
        intersect_walls = [intersect_walls_point, self.collision_with_wall]
        if dist(intersect_walls[0], self.pos) < dist(intersection[0], self.pos):
            intersection = intersect_walls

        intersect_enemy_point, shooted_enemy = self.is_colliding_with_enemies(trajectory)
        intersect_enemies = [intersect_enemy_point, self.collision_with_enemy]
        if dist(intersect_enemies[0], self.pos) < dist(intersection[0], self.pos):
            intersect_enemies[1](intersect_enemies[0], shooted_enemy)
        elif intersection[0] is not None:
            intersection[1](intersection[0])

    def is_colliding_with_enemies(self, trajectory):
        """
        Метод обработки коллизий с Enemy, находящимися поблизости

        :param trajectory: отрезок из текущей и следующей позиции пули
        :return: (Point близжайшей коллизии(None, если коллизии нет), Enemy, с которым произошла коллиия)
        """
        intersection_point = None
        shooted_enemy = None
        middle = (trajectory.p2 + trajectory.p1) / 2
        neighbours = self.scene.plane.get_neighbours(middle)
        for neighbour in neighbours:
            if neighbour.type == 'Enemy':
                distance = dist(neighbour.pos, self.pos)
                slash_distance = neighbour.HITBOX_RADIUS + 5
                if distance < slash_distance:
                    shooted_enemy = neighbour
        return intersection_point, shooted_enemy

    def collision_with_enemy(self, enemy):
        """
        Метод, выполняемый в случае коллизии с Enemy

        :param intersection_point: точка пересечения с Enemy
        :param enemy: Enemy, в которого попала пуля
        """
        enemy.get_damage(self.damage)
        self.scene.game_objects.append(Slash_Animation(self.scene, self.controller, self.pos, self.angle))
        self.destroy()

    def collision_with_wall(self, intersection_point):
        """
        Метод, выполняемый в случае коллизии со стеной

        :param intersection_point: точка пересечения со стеной
        """

        self.scene.game_objects.append(Slash_Animation(self.scene, self.controller, self.pos, self.angle))
        self.destroy()


class Slash_Animation(GameSprite):
    IMAGE_NAMES = [
        'moving_objects.melee_weapon.attack.heavy_splash.1',
        'moving_objects.melee_weapon.attack.heavy_splash.2',
        'moving_objects.melee_weapon.attack.heavy_splash.3',
    ]
    IMAGE_ZOOMS = [0.4, 0.4, 0.4]

    def __init__(self, scene: Scene, controller: Controller, pos: Point, angle: float = 0):
        pos = pos - vector_from_length_angle(8, angle)
        super().__init__(scene, controller, Slash_Animation.IMAGE_NAMES[0], pos, angle, Slash_Animation.IMAGE_ZOOMS[0])
        self.image_ind = 0

    def process_logic(self):
        self.image_name = Slash_Animation.IMAGE_NAMES[self.image_ind // 4]
        self.zoom = Slash_Animation.IMAGE_ZOOMS[self.image_ind // 4]
        self.image_ind += 1
        if self.image_ind >= len(Slash_Animation.IMAGE_NAMES) * 4:
            self.destroy()
