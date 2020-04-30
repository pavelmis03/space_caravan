class Timer:
    """
    Класс для замера времени (пока в циклах)
    """
    def __init__(self, time: int):
        self.__is_started = False
        self.__time = time

    def start(self):
        """
        Начать таймер
        """
        self.__is_started = True

    @property
    def is_started(self):
        return self.__is_started

    @property
    def is_alarm(self):
        """
        прошло ли отведенное время
        """
        return not self.__time

    def process_logic(self):
        """
        Тик таймера.
        """
        if self.__is_started and not self.is_alarm:
            self.__time -= 1

EMPTY_TIMER = Timer(1) #таймер-заглушка. Он не запущен, поэтому никогда не будет is_alarm