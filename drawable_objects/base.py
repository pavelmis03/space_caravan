import pygame

from geometry.point import Point
from controller.controller import Controller
from scenes.base import Scene
from utils.image import ImageManager

from geometry.distances import dist
from math import cos
from math import sin


class AbstractObject:
    """
        Базовый класс объекта, хранящегося как поле у сцены. Подходит для наследования от него классов не видимых
        на сцене объектов.

        :param scene: сцена объекта
        :param controller: ссылка на объект контроллера
        """

    def __init__(self, scene: Scene, controller: Controller):
        self.scene = scene
        self.controller = controller

    def process_logic(self):
        """
        Исполнение логики объекта.
        """
        pass

    def process_draw(self):
        """
        Отрисовка объекта.
        """
        pass


class SurfaceObject(AbstractObject):
    """
    Отдельный класс для отрисовки уже отреднеренной surface.
    Используется для отрисовки статичной предподсчитанной графики (то есть той, которая
    не двигается). Не стоит путать со SpriteObject'ом, который не двигается относительно экрана.

    Не нужно использовать объект этого класса для других целей, он хранит
    в себе картинку, а значит, потребляет много памяти.
    """

    def __init__(self, surface: pygame.Surface, scene: Scene, controller: Controller, pos: Point):
        super().__init__(scene, controller)
        self.surface = surface
        self.pos = pos

    def process_draw(self):
        relative_center = self.scene.relative_center
        relative_pos = self.pos - relative_center
        ImageManager.draw_surface(
            self.surface, relative_pos, self.scene.screen)


class DrawableObject(AbstractObject):
    """
    Базовый класс отрисовываемого объекта. Имеет абсолютную позицию на экране, не имеет текстуры. Подходит для
    наследования от него объектов пользовательского интерфейса без текстуры.

    :param scene: сцена объекта
    :param controller: ссылка на объект контроллера
    :param pos: координаты объекта
    """

    def __init__(self, scene: Scene, controller: Controller, pos: Point):
        super().__init__(scene, controller)
        self.pos = pos

    def move(self, new_pos):
        """
        Перемещение объекта.

        :param new_pos: новое положение
        """
        self.pos = new_pos


class SpriteObject(DrawableObject):
    """
    Базовый класс объекта с текстурой. Имеет абсолютную позицию на экране и угол поворота.

    :param scene: сцена объекта
    :param controller: ссылка на объект контроллера
    :param image_name: имя картинки в базе менеджера
    :param pos: координаты объекта
    :param angle: угол поворота объекта
    :param zoom: масштаб картинки
    """

    def __init__(self, scene: Scene, controller: Controller, image_name: str,
                 pos: Point, angle: float = 0, zoom: float = 1):
        super().__init__(scene, controller, pos)
        self.image_name = image_name
        self.angle = angle
        self.zoom = zoom

    def process_draw(self):
        ImageManager.process_draw(
            self.image_name, self.pos, self.scene.screen, self.zoom, self.angle)

    def collides_with(self, other_object):
        """
        Проверка на коллизию через pygame. Вроде бесполезно, но пока оставим.

        :param other_object: другой объект для проверки на коллизию
        """
        return pygame.sprite.collide_mask(self, other_object)


class GameSprite(SpriteObject):
    """
    Базовый класс объекта на игровом уровне. Отрисовывается на сцене в относительных координатах. Взаимодействует с
    GamePlane - плоскостью игрового мира. Может быть создан на сцене в процессе игры, может быть удален в процессе
    игры (метод destroy).

    :param scene: сцена объекта
    :param controller: ссылка на объект контроллера
    :param image_name: имя картинки в базе менеджера
    :param pos: координаты объекта
    :param angle: угол поворота объекта
    :param zoom: масштаб картинки
    """

    def __init__(self, scene: Scene, controller: Controller, image_name: str, pos: Point, angle: float = 0,
                 zoom: float = 1):
        super().__init__(scene, controller, image_name, pos, angle, zoom)
        self.scene.plane.insert(self, self.pos)
        self.enabled = True
        self.rotation_offset = None

    def destroy(self):
        """
        Уничтожение игрового объекта. Будет уничтожен на ближайшей итерации своей сценой.
        """
        self.enabled = False

    def process_draw(self):
        """
        Отрисовка объекта в относительных координатах

        Если объект вне экрана, он не отрисовывается
        relative_center: центр относительных координат
        """
        relative_center = self.scene.relative_center
        relative_pos = self.pos - relative_center

        if ImageManager.is_out_of_screen(self.image_name, self.zoom,
                                         relative_pos, self.scene.game.screen_rectangle):
            return

        ImageManager.process_draw(self.image_name, relative_pos,
                                  self.scene.screen, self.zoom, self.angle, self.rotation_offset)

    def move(self, new_pos):
        self.scene.plane.do_step(self, self.pos, new_pos)
        self.pos = new_pos


class Humanoid(GameSprite):
    """
    Базовый класс человекоподобного существа: это объект на уровне с текстурой, у которого круглый хитбокс.
    """
    HITBOX_RADIUS = 25


class UsableObject(GameSprite):
    """
    Базовый класс объекта, с которым игрок может взаимодействовать на клавишу ACTIVATION_KEY,
    подойдя на определенное расстояние
    """
    ACTIVATION_KEY = pygame.K_e

    def __init__(self, scene: Scene, controller: Controller, image_name: str, pos: Point, angle: float = 0,
                 zoom: float = 1, usage_radius: float = 100):
        super().__init__(scene, controller, image_name, pos, angle, zoom)
        # Радиус вокруг объекта, в пределах которого с ним можно взаимодействовать
        self.usage_radius = usage_radius

    def process_logic(self):
        super().process_logic()
        if dist(self.scene.player.pos, self.pos) <= self.usage_radius:  # Проверка активации
            if self.controller.is_key_pressed(key=UsableObject.ACTIVATION_KEY):
                self.activate()

    def activate(self):
        """
        Функция, активирующаяся при взаимодействии с объектом
        """

        x_speed = cos(self.angle) * self.speed
        y_speed = -sin(self.angle) * self.speed
        return Point(x_speed, y_speed)
