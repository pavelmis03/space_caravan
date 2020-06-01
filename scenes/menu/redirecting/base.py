from scenes.menu.base import MenuScene
from utils.timer import Timer
from constants.color import COLOR


class RedirectingScene(MenuScene):
    """
    Базовый класс перенаправляющей сцены меню. Выводит на экран текст; по истечении заданного времени выполняет
    перенаправление на другую сцену. В некоторый заданный момент выводит подсказку для пользователя и позволяет
    перейти на другую сцену по клику мыши. Перенаправляющая сцена не может сохраняться как сцена меню.

    :param game: игра, создающая сцену
    """

    DELAY_BEFORE_REDIRECTION = 500
    DELAY_BEFORE_CLICK = 100

    DESCRIPTION = ''
    PROMPT = 'Кликните, чтобы пропустить...'
    TEXT_COLOR = COLOR['LIGHT_RED']
    ALIGN = 'center'
    FONT_SIZE = 80
    PROMPT_FONT_SIZE = 15

    def __init__(self, game):
        super().__init__(game)
        self.menu.add_multilinetext(self.DESCRIPTION, color=self.TEXT_COLOR, align=self.ALIGN,
                                    font_name='freesansbold', font_size=self.FONT_SIZE, is_bold=False)
        self.prompt_shown = False

        self.redirection_timer = Timer(self.DELAY_BEFORE_REDIRECTION)
        self.click_timer = Timer(self.DELAY_BEFORE_CLICK)
        self.redirection_timer.start()
        self.click_timer.start()

    def show_prompt(self):
        """
        Вывод подсказки для пользователя.
        """
        self.prompt_shown = True
        self.menu.add_multilinetext(self.PROMPT, color=self.TEXT_COLOR, align=self.ALIGN,
                                    font_name='freesansbold', font_size=self.PROMPT_FONT_SIZE, is_bold=False)

    def timers_logic(self):
        """
        Логика таймеров сцены.
        """
        self.redirection_timer.process_logic()
        self.click_timer.process_logic()
        if self.click_timer.is_alarm and not self.prompt_shown:
            self.show_prompt()
        if self.click_timer.is_alarm and self.game.controller.click_pos:
            self.redirect()
        if self.redirection_timer.is_alarm:
            self.redirect()

    def process_all_logic(self):
        super().process_all_logic()
        self.timers_logic()

    def redirect(self):
        """
        Метод, вызывающийся сценой для перенаправления на другую.
        """
        pass
