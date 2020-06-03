Использованные паттерны проектирования
======================================

Стратегия
---------

* controller -> :ref:`controller.controller`
* drawable_objects -> :ref:`drawable_objects.menu.text`

Состояние
---------

* drawable_objects -> :ref:`drawable_objects.enemy`

Шаблонный метод
---------------

* utils -> :ref:`utils.is_marked_manager`

Цепочка обязанностей
--------------------

* enemy_interaction_with_grid -> :ref:`enemy_interaction_with_grid.manager` и классы-помощники из
  :ref:`enemy_interaction_with_grid.hearing.manager` и :ref:`enemy_interaction_with_grid.vision.manager`

Фасад
-----

* map -> :ref:`map.level.grid` вместе с методами предков

Декоратор
---------

* map -> :ref:`map.grid`
* drawable_objects -> :ref:`drawable_objects.enemy`

