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
    VOLUME = {
        'ui.select': 0.08,
        'ui.press1': 0.08,
        'ui.press2': 0.08,
        'ui.keytype': 0.8,

        'weapon.slot': 0.15,

        'weapon.attack.pistol': 0.15,
        'weapon.attack.shotgun': 0.04,
        'weapon.attack.rifle1': 0.04,
        'weapon.attack.rifle2': 0.1,
        'weapon.attack.sword': 0.15,
        'weapon.attack.fist': 0.15,

        'weapon.reload.pistol': 0.08,
        'weapon.reload.shotgun': 0.08,
        'weapon.reload.rifle1': 0.08,
        'weapon.reload.rifle2': 0.08,

        'usable.pickup': 0.15,
        'usable.chest': 0.4,

        'humanoid.death': 0.15,
    }

    @staticmethod
    def configure_volume():
        """
        Установка конкретных значений, что бы звуки были
        примерно одной громкости
        """
        for name, volume in SoundManager.VOLUME.items():
            SoundManager.set_volume(name, volume)

    @staticmethod
    def load_all():
        """
        по умолчанию считает, что все звуки wav.
        """
        SoundManager.load_dir(SoundManager.SOUND_PATH)

    @staticmethod
    def load_dir(directory: str, extension: str = '.wav'):
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
                SoundManager.load_dir(full_item, extension)
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

    @staticmethod
    def set_volume(sound_path: str, value: float = 1):
        """
        Изменение громкости звука
        :param sound_path: имя звука (путь к нему)
        :param value: значение
        :return:
        """
        sound = SoundManager.get_sound(sound_path)
        if isinstance(sound, dict):
            raise ValueError(sound + ' is a dir, not a file')
        sound.set_volume(value)
