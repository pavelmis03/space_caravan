from math import sqrt
from drawable_objects.base import GameSprite
from geometry.point import Point
#from geometry.distances import dist
from geometry.segment import Segment
from geometry.circle import Circle
from geometry.intersections import intersect_seg_circle
#from geometry.intersections import intersect_line_circle
from geometry.vector import vector_from_length_angle, length
from geometry.line import line_from_points
from scenes.base import Scene
from controller.controller import Controller
#from geometry.distances import dist
from utils.game_plane import GamePlane
from geometry.distances import vector_dist_point_seg
from geometry.line import Line


def create_bullet(shooter: GameSprite):
    bullet = Bullet(shooter.scene, shooter.controller, shooter.pos, shooter.angle)
    shooter.scene.game_objects.append(bullet)

def dist(p1: Point, p2: Point) -> float:
    """
    Расстояние между точками.

    :param p1: первая точка
    :param p2: вторая точка
    :return: числовое значение
    """
    if p1 is None or p2 is None:
        return 100000000
    return length(p2 - p1)


class Bullet(GameSprite):

    IMAGE_ZOOM = 0.7
    IMAGE_NAME = 'moving_objects.bullet.1' # нужно перерисовать
    SPEED = 100

    def __init__(self, scene: Scene, controller: Controller, pos: Point, angle: float = 0):
        super().__init__(scene, controller, Bullet.IMAGE_NAME, pos, angle, Bullet.IMAGE_ZOOM)
        self.direction = vector_from_length_angle(Bullet.SPEED, self.angle)

    def process_logic(self):
        next_pos = self.pos + self.direction
        self.collision_manager(next_pos)
        #self.scene.game_objects.append(Collision_Point(self.scene, self.controller, self.pos, self.angle))
        self.move(next_pos)

    def poop(self, a, b):
        print(a, b)

    def collision_manager(self, next_pos: Point):
        trajectory = Segment(self.pos, next_pos)

        intersect_player_point = self.is_colliding_with_player(trajectory)
        intersect_player = [intersect_player_point, self.collision_with_player]
        intersection = intersect_player

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

    def is_colliding_with_player(self, tragectory: Segment):
        player = Circle(self.scene.player.pos, self.scene.player.HITBOX_RADIUS)
        intersection_point = intersect_seg_circle(tragectory, player)
        return intersection_point

    def is_colliding_with_enemies(self, tragectory):
        intersection_point = None
        shooted_enemy = None
        middle = (tragectory.p2 + tragectory.p1) / 2
        neighbours = self.scene.plane.get_neighbours(tragectory.p2)
        for neighbour in neighbours:
            if neighbour.type == 'Enemy':
                enemy_circle = Circle(neighbour.pos, neighbour.HITBOX_RADIUS + 1)
                neighbour_intersection_point = intersect_seg_circle(tragectory, enemy_circle)
                distance = dist(self.pos, neighbour_intersection_point)
                if distance < dist(self.pos, intersection_point):
                    shooted_enemy = neighbour
                    intersection_point = neighbour_intersection_point

        neighbours = self.scene.plane.get_neighbours(tragectory.p1)
        for neighbour in neighbours:
            if neighbour.type == 'Enemy':
                enemy_circle = Circle (neighbour.pos, neighbour.HITBOX_RADIUS + 1)
                neighbour_intersection_point = intersect_seg_circle(tragectory, enemy_circle)
                distance = dist(self.pos, neighbour_intersection_point)
                if distance < dist (self.pos, intersection_point):
                    shooted_enemy = neighbour
                    intersection_point = neighbour_intersection_point

        return intersection_point, shooted_enemy

    def collision_with_enemy(self, intersection_point, enemy):
        #self.scene.plane.erase(enemy, enemy.pos)
        #enemy.destroy()
        self.scene.game_objects.append(Collision_Point(self.scene, self.controller, intersection_point, self.angle))
        self.destroy()

    def collision_with_player(self, intersection_point):
        self.scene.player.destroy()
        self.scene.game_objects.append(Collision_Point(self.scene, self.controller, intersection_point, self.angle))
        self.destroy()

    def collision_with_wall(self, intersection_point):
        self.scene.game_objects.append(Collision_Point(self.scene, self.controller, intersection_point, self.angle))
        self.destroy()


class Collision_Point(Bullet):
    IMAGE_ZOOM = 0.5

    def __init__(self, scene: Scene, controller: Controller, pos: Point, angle: float = 0):
        self.speed = 0
        self.bullet_type = 'bullet'
        self.lifetime = 20
        angle = angle
        super().__init__(scene, controller, pos, angle)

    def process_logic(self):
        self.lifetime -= 1
        if (self.lifetime <= 0):
            self.destroy()
        pass
