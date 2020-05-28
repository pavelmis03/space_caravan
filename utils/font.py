import os

import pygame


class FontManager:
    """
    Загружает необходимы шрифты
    Необходим что бы заменить pygame.font.SysFont
    на pygame.font.Font
    """
    FONT_PATH = 'fonts'

    @staticmethod
    def get_font(font_name: str, size: int) -> pygame.font.Font:
        font = os.path.join(FontManager.FONT_PATH, font_name.lower())
        font += '.ttf'
        return pygame.font.Font(font, size)
