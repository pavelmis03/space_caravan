from drawable_objects.base import GameSprite
from drawable_objects.enemy import Enemy
from geometry.point import Point
from geometry.segment import Segment
from geometry.circle import Circle
from geometry.intersections import intersect_seg_circle
from geometry.vector import vector_from_length_angle, length
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


class Bullet(GameSprite):
    """
    Базовая пуля (далека от завершения).

    :param weapon: оружие, создавшее пулю
    :param pos: начальная позиция пули
    :param angle: начальный угол направления пули
    """

    def __init__(self, weapon, pos: Point, angle: float, damage, speed, image_name, image_zoom=1):
        super().__init__(weapon.scene, weapon.controller, image_name, pos, angle, image_zoom)
        self.direction = vector_from_length_angle(speed, self.angle)
        self.damage = damage
        self.is_hurting_enemies = weapon.owner.__class__.__name__ != 'Enemy'
        self.invisibility_time = 1

    def process_draw(self):
        """
        Отрисовка объекта в относительных координатах

        Перегружен, чтобы пуля рисовалась чуть заднее своего pos, так как
        при близости к стенам её кончик будто находится внутри

        Если объект вне экрана, он не отрисовывается
        relative_center: центр относительных координат
        """
        if self.invisibility_time:
            self.invisibility_time -= 1
        else:
            pos = self.pos - vector_from_length_angle(
                ImageManager.get_width(self.image_name, self.zoom) // 2, self.angle)
            relative_center = self.scene.relative_center
            relative_pos = pos - relative_center
            if ImageManager.is_out_of_screen(self.image_name, self.zoom,
                                             relative_pos, self.scene.game.screen_rectangle):
                return
            ImageManager.process_draw(self.image_name, relative_pos,
                                      self.scene.screen, self.zoom, self.angle, self.rotation_offset)

    def process_logic(self):
        next_pos = self.pos + self.direction
        self.collision_manager(next_pos)
        self.move(next_pos)

    def collision_manager(self, next_pos: Point):
        """
        Метод обработки всех возможных коллизий, нахождения близжайшей из них к pos пули
        и выполнения соответствующего виду коллизии метода

        :param next_pos: следующая позиция
        """
        trajectory = Segment(self.pos, next_pos)

        intersect_player_point = self.is_colliding_with_player(trajectory)
        intersect_player = [intersect_player_point, self.collision_with_player]
        intersection = intersect_player

        intersect_walls_point = self.scene.grid.intersect_seg_walls(trajectory)
        intersect_walls = [intersect_walls_point, self.collision_with_wall]
        if dist(intersect_walls[0], self.pos) < dist(intersection[0], self.pos):
            intersection = intersect_walls

        intersect_enemy_point, shooted_enemy = self.is_colliding_with_enemies(
            trajectory)
        intersect_enemies = [intersect_enemy_point, self.collision_with_enemy]
        if dist(intersect_enemies[0], self.pos) < dist(intersection[0], self.pos):
            intersect_enemies[1](intersect_enemies[0], shooted_enemy)
        elif intersection[0] is not None:
            intersection[1](intersection[0])

    def is_colliding_with_player(self, tragectory: Segment):
        """
        Метод обработки коллизий с Player

        :param tragectory: отрезок из текущей и следующей позиции пули
        :return: Point коллизии или None, если коллизии нет
        """
        player = Circle(self.scene.player.pos, self.scene.player.HITBOX_RADIUS)
        intersection_point = intersect_seg_circle(tragectory, player)
        return intersection_point

    def is_colliding_with_enemies(self, tragectory):
        """
        Метод обработки коллизий с Enemy, находящимися поблизости

        :param tragectory: отрезок из текущей и следующей позиции пули
        :return: (Point близжайшей коллизии(None, если коллизии нет), Enemy, с которым произошла коллиия)
        """
        if not self.is_hurting_enemies:
            return None, None
        intersection_point = None
        shooted_enemy = None
        middle = (tragectory.p2 + tragectory.p1) / 2
        neighbours = self.scene.plane.get_neighbours(middle, Enemy)
        for neighbour in neighbours:
            enemy_circle = Circle(neighbour.pos, neighbour.HITBOX_RADIUS)
            neighbour_intersection_point = intersect_seg_circle(
                tragectory, enemy_circle)
            distance = dist(self.pos, neighbour_intersection_point)
            if distance < dist(self.pos, intersection_point):
                shooted_enemy = neighbour
                intersection_point = neighbour_intersection_point
        return intersection_point, shooted_enemy

    def collision_with_enemy(self, intersection_point, enemy):
        """
        Метод, выполняемый в случае коллизии с Enemy

        :param intersection_point: точка пересечения с Enemy
        :param enemy: Enemy, в которого попала пуля
        """
        enemy.get_damage(self.damage, self.angle)
        self.destroy()

    def collision_with_player(self, intersection_point):
        """
        Метод, выполняемый в случае коллизии с Player

        :param intersection_point: точка пересечения с Player
        """
        self.scene.game_objects.append(CollisionAnimation(self.scene, self.controller, intersection_point, self.angle))
        self.scene.player.get_damage(self.damage, self.angle)
        self.destroy()

    def collision_with_wall(self, intersection_point):
        """
        Метод, выполняемый в случае коллизии со стеной

        :param intersection_point: точка пересечения со стеной
        """
        self.scene.game_objects.append(CollisionAnimation(
            self.scene, self.controller, intersection_point, self.angle))
        self.destroy()


class ShotgunBullet(Bullet):

    def __init__(self, weapon, pos, angle, damage):
        speed = 120
        image_name = 'moving_objects.bullet.shotgun_bullet'
        zoom = 0.6
        super().__init__(weapon, pos, angle, damage, speed,
                         image_name,  zoom)


class PistolBullet(Bullet):

    def __init__(self, weapon, pos, angle, damage):
        speed = 150
        image_name = 'moving_objects.bullet.pistol_bullet'
        zoom = 0.55
        super().__init__(weapon, pos, angle, damage, speed,
                         image_name, zoom)


class RifleBullet(Bullet):

    def __init__(self, weapon, pos, angle, damage):
        speed = 170
        image_name = 'moving_objects.bullet.rifle_bullet'
        zoom = 0.6
        super().__init__(weapon, pos, angle, damage, speed,
                         image_name, zoom)


class CollisionAnimation(GameSprite):

    IMAGE_NAMES = [
        'moving_objects.bullet.2',
        'moving_objects.bullet.6',
    ]
    IMAGE_ZOOMS = [0.7, 1.8]

    def __init__(self, scene, controller, pos: Point, angle: float = 0):
        pos = pos - vector_from_length_angle(8, angle)
        super().__init__(scene, controller,
                         CollisionAnimation.IMAGE_NAMES[0], pos, angle, CollisionAnimation.IMAGE_ZOOMS[0])
        self.image_ind = 0
        self.one_frame_vision_time = 3

    def process_logic(self):
        self.image_name = CollisionAnimation.IMAGE_NAMES[self.image_ind // self.one_frame_vision_time]
        self.zoom = CollisionAnimation.IMAGE_ZOOMS[self.image_ind // self.one_frame_vision_time]
        self.image_ind += 1
        if self.image_ind >= len(CollisionAnimation.IMAGE_NAMES) * self.one_frame_vision_time:
            self.destroy()


BULLET_CLASS = {
    'Shotgun': ShotgunBullet,
    'Pistol': PistolBullet,
    'Rifle': RifleBullet,
}
