from typing import List, Dict

from drawable_objects.interface.ammo_display import AmmoDisplay
from drawable_objects.interface.essence_display import EssenceDisplay
from drawable_objects.interface.pause_manager import PauseManager
from drawable_objects.interface.player_icon import PlayerIcon
from drawable_objects.interface.weapons_display import WeaponsDisplay
from drawable_objects.player import Player
from drawable_objects.usable_object import UsableObject
from drawable_objects.base import DrawableObject
from geometry.point import Point
from scenes.game.base import GameScene
from utils.camera import Camera
from utils.timer import Timer
from utils.game_plane import GamePlane
from utils.game_data_manager import from_list_of_dicts, to_list_of_dicts


def delete_destroyed(objects: List[any]):
    """
    Быстрое удаление уничтоженных эл-тов (который not enabled).
    Так как мы меняем местами удаляемый эл-т и делаем pop, работает за O(n).

    :param objects: список объектов
    """
    i = 0
    while i < len(objects):
        if not objects[i].enabled:
            objects[i], objects[-1] = objects[-1], objects[i]
            objects.pop()
            continue
        i += 1


class LevelScene(GameScene):
    """
    Базовый класс сцены уровня. Содержит игрока, сетку и прочие элементы игрового уровня.

    :param game: игра, создающая сцену
    :param data_filename: имя файла, в который сохраняется сцена (расширение не указывать)
    """
    FIXED_CAMERA = False
    PLAYER_SPAWN_POINT = Point(100, 100)

    def __init__(self, game, data_filename: str):
        super().__init__(game, data_filename)
        self.game_objects = []
        self.enemies = []
        self.relative_center = Point(0, 0)
        self.pause_object = None
        self.plane = GamePlane()
        self.grid = None
        self.player = None
        self.pause_manager = PauseManager(self, self.game.controller)
        self.camera = Camera(self)

        self.e_timer = Timer(UsableObject.ACTIVATION_COOLDOWN)  # таймер для "перезарядки" кнопки E
        self.e_timer.start()

    def to_dict(self) -> Dict:
        result = super().to_dict()
        result.update({
            'game_objects': to_list_of_dicts(self.game_objects),
            'enemies': to_list_of_dicts(self.enemies),
        })
        return result

    def from_dict(self, data_dict: Dict):
        super().from_dict(data_dict)
        self.game_objects += from_list_of_dicts(self,
                                                data_dict['game_objects'])
        self.enemies += from_list_of_dicts(self, data_dict['enemies'])

    def create_state_display(self):
        """
        Создание объектов, отображающих состояние игрока и его оружия.
        """
        player_icon = PlayerIcon(self, self.game.controller, self.player)
        self.interface_objects.append(player_icon)
        weapons_display = WeaponsDisplay(self.player, Point(100, 0))
        self.interface_objects.append(weapons_display)
        ammo_display = AmmoDisplay(self, self.game.controller, Point(240, 20), self.player.weapon)
        self.interface_objects.append(ammo_display)

    def load_player(self):
        """
        Загрузка игрока (он хранится отдельно от сцен). Вызывается автоматически в Game.
        """
        self.player = Player(self, self.game.controller, Point(0, 0))
        self.player.load()
        self.player.move(self.PLAYER_SPAWN_POINT)
        self.create_state_display()

    def load_common_data(self):
        super().load_common_data()
        essence_display = EssenceDisplay(self, self.game.controller, (1, 0), self.common_data)
        self.interface_objects.append(essence_display)

    def save(self):
        super().save()
        self.player.save()

    def pause(self, pause_object: DrawableObject):
        """
        Пауза игры.

        :param pause_object: объект, ставящий игру на паузу; этот объект не должен быть в interface_objects,
            его отрисовка и логика будут вызываться отдельно все то время, пока игра на паузе
        """
        self.pause_object = pause_object

    def resume(self):
        """
        Продолжение игры после паузы.
        """
        self.pause_object = None

    def update_relative_center(self):
        """
        Обновление центра относительных координат сцены. Чтобы управление персонажем было наиболее удобным,
        должно вызываться в правильный момент: после перемещение персонажа по клавишам, но перед его поворотом
        к мыши.
        """
        self.relative_center = self.camera.get_relative_center(
            not LevelScene.FIXED_CAMERA)

    def game_logic(self):
        """
        Игровая логика в следующем порядке: сетка, игровые объекты и враги, игрок.
        """
        self.grid.process_logic()

        for item in self.game_objects:
            item.process_logic()
        for item in self.enemies:
            self.grid.save_enemy_pos(item.pos)
        for item in self.enemies:
            item.process_logic()

        self.player.process_logic()

    def interface_logic(self):
        super().interface_logic()
        self.pause_manager.process_logic()

    def delete_destroyed_objects(self):
        """
        Удаление уничтоженных элементов.
        """
        delete_destroyed(self.game_objects)
        delete_destroyed(self.enemies)

    def process_all_logic(self):
        if not self.pause_object:
            super().process_all_logic()
            self.game_logic()
        else:
            self.pause_object.process_logic()

        self.delete_destroyed_objects()
        self.e_timer.process_logic()

    def game_draw(self):
        """
        Игровая отрисовка в следующем порядке: сетка, игровые объекты и враги, игрок.
        """
        self.grid.process_draw()

        for item in self.game_objects:
            item.process_draw()
        for item in self.enemies:
            item.process_draw()

        self.player.process_draw()

    def process_all_draw(self):
        self.clear_screen()
        self.game_draw()
        self.interface_draw()
        if self.pause_object:
            self.pause_object.process_draw()
