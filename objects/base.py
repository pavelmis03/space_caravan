import pygame


class DrawObject:
    def __init__(self, game):
        self.game = game

    def process_event(self, event):
        pass

    def process_logic(self):
        pass

    def process_draw(self):
        pass


class SpriteObject(DrawObject):
    def __init__(self, game):
        super().__init__(game)

    def resize(self, percents):
        # resizing self.image in (0, 1)
        rect = self.image.get_rect()
        size = (
            int(rect.width * percents),
            int(rect.height * percents)
        )
        self.image = pygame.transform.scale(self.image, size)