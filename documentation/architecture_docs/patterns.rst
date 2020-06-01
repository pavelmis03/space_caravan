Использованные паттерны проектирования
======================================

Стратегия
---------
controller.controller
drawable_objects.menu.text

Состояние
---------
drawable_objects.enemy

Шаблонный метод
---------------
utils.is_marked_manager

Цепочка обязанностей
--------------------
enemy_interaction_with_grid.manager...

Фасад
-----
map.level.grid (вместе с методами предков) - фасад

Декоратор
---------
map.grid и map.grid_index_manager
map.collision_grid.collision_grid
map.collision_grid.draw_static_manager
map.collision_grid.intersection_manager)
map.level.grid и (map.level.map_generator, map.level.objects_generator)
