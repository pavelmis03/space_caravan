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
    def __init__(self, game, filename):
        super().__init__(game)
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()

    def resize(self, percents):
        # resizing self.image in (0, 1)
        rect = self.image.get_rect()
        size = (
            int(rect.width * percents),
            int(rect.height * percents)
        )
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()

    def process_draw(self):
        self.game.screen.blit(self.image, self.rect)

    def collides_with(self, other_object):
        return pygame.sprite.collide_mask(self, other_object)