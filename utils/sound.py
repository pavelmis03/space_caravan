"""
Все, что связано с загрузкой и проигрыванием музыки и звуков
"""
import os

import pygame



class SoundManager:

    """
    Загружает все звуки/музыку и осуществляет быстрый доступ к ним а так же работу с ними
    Возможна рекурсивная загруска всех wav картинок
    """
    sounds = {}
    SOUND_PATH = 'sounds'

    @staticmethod
    def load_all():
        """
        по умолчанию считает, что все звуки wav.
        """
        SoundManager.load_dir(SoundManager.SOUND_PATH)

    @staticmethod
    def load_dir(directory: str, extension: str='.wav'):
        """
        Загрузка всех файлов расширения extension из директории рекурсивно
        :param directory: директория
        :param extension: расширение загружаемых файлов (wav или ogg)
        """
        for item in os.listdir(directory):
            full_item = os.path.join(directory, item)
            short_dir = directory.replace(
                SoundManager.SOUND_PATH, '').strip(os.sep)
            if os.path.isdir(full_item):
                manager_dir = SoundManager.get_sound(short_dir, os.sep)
                manager_dir[item] = {}
                SoundManager.load_dir(full_item)
            elif extension in item:
                manager_dir = SoundManager.get_sound(short_dir, os.sep)
                item = item.replace(extension, '')
                manager_dir[item] = pygame.mixer.Sound(full_item)

    @staticmethod
    def get_sound(path: str, delimiter: str = '.'):
        """
        Данная функция нужна для удобного получения файлов из
        SoundManager.sounds
        Может так же и возвращать словари с звуками при указании неполного пути

        :param path: путь до звука, выглядит примерно как
            папка.папка.файл (файл без расширения, начало папок из sounds)
        :param delimiter: разделитель между папками и изображениями
            по умолчанию используется точка (aka python style),
            но можно и делить по другому, слешы крайне НЕ рекомендуются
        """
        res = SoundManager.sounds
        if not path:
            return res
        for item in path.split(delimiter):
            if item in res:
                res = res[item]
            else:
                raise ValueError(item + ' not found in path ' + path)
        return res

    @staticmethod
    def play_sound(sound_path: str):
        sound = SoundManager.get_sound(sound_path)
        if isinstance(sound, dict):
            raise ValueError(sound + ' is a dir, not a file')
        sound.play()