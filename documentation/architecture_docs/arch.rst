Архитектура проекта
===================

Общие положения
---------------

.. image:: /_static/Common.jpg

Главный класс проекта - Game. У него есть ссылки на объекты трех классов, представляющие разные области проекта:
массив Scene, Space и Controller. Каждая Scene - игровая сцена (менюшка, уровень, карты неба и т. д.). Space -
класс, содержащий информацию об игровом мире. Controller - класс, обрабатывающий события клавиатуры и мыши,
запоминающий состояние клавиш и все такое.

Информация о классах
--------------------

Написанное здесь фиксирует в основном вненшие зависимости для классов, то есть те поля и методы, которые будут
использоваться извне объектами других классов. Реализация неописанных внутренних функций класса на усмотрение
разработчика.

* class DrawableObject:
    * def __init__(controller)
    * def process_logic()
    * def process_draw()

* class Game:
    * def __init__(window_width, window_height)
    * def create_window()
    * def main_loop()
    * def set_scene(scene_index)
    * running: bool  # Продолжать ли главный цикл
    * scenes: Scene[]  # Массив сцен

* class Controller:
    * def __init__()
    * def process_event()
    * is_key_pressed(char key)
    * get_mouse_position()
    * get_mouse_click()
    * key_state: bool[]  # Массив состояний клавиш
