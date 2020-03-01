import pygame

from drawable_objects.base import DrawableObject


class Text(DrawableObject):
    ALIGNS = {
        'left',
        'center',
    }

    def __init__(self, scene, pos, text='Define me!', color=(255, 255, 255), align='left', font_name='Comic Sans',
                 font_size=35, is_bold=True, is_italic=False):
        super().__init__(scene, None, pos)
        self.color = color
        if align in Text.ALIGNS:
            self.align = align
        else:
            self.align = 'left'
        self.font = pygame.font.SysFont(font_name, font_size, is_bold, is_italic)
        self.text = None
        self.text_surface = None
        self.update_text(text)

    def update_text(self, text):
        self.text = text
        self.text_surface = self.font.render(self.text, True, self.color)

    def process_draw(self):
        rect = self.text_surface.get_rect()
        if self.align == 'left':
            rect.left = self.pos.x
            rect.top = self.pos.y
        if self.align == 'center':
            rect.centerx = self.pos.x
            rect.centery = self.pos.y
        self.scene.screen.blit(self.text_surface, rect)

        pygame.rect
