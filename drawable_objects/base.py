import pygame


class DrawableObject:
    """
    Базовый класс отрисовываемого объекта.

    :param controller: ссылка на объект контроллера
    """
    def __init__(self, controller):
        self.controller = controller

    def process_logic(self):
        """
        Исполнение логики объекта.
        """
        pass

    def process_draw(self, screen):
        """
        Отрисовка объекта.
        """
        pass


class SpriteObject(DrawableObject):
    """
    Базовый класс объекта с текстурой.

    :param controller: ссылка на объект контроллера (пока None)
    :param filename: имя файла с текстурой
    """
    def __init__(self, controller, filename):
        super().__init__(controller)
        self.image = pygame.image.load(filename)

    def resize(self, percents):
        """
        Установить размер текстуры в некоторую долю от исходного.

        :param percents: доля исходного размера (десятичная дробь)
        """
        rect = self.image.get_rect()
        size = (
            int(rect.width * percents),
            int(rect.height * percents)
        )
        self.image = pygame.transform.scale(self.image, size)

    def process_draw(self, screen):
        rect = self.image.get_rect()
        screen.blit(self.image, rect)

    def collides_with(self, other_object):
        """
        Проверка на коллизию через pygame. Вроде бесполезно, но пока оставим.

        :param other_object: другой объект для проверки на коллизию
        """
        return pygame.sprite.collide_mask(self, other_object)