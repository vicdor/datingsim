import pygame

def center_text(text, font, font_color, rect, surf):
    """blits the text into the center of rect on surf"""
    t_surf = font.render(text, False, font_color)
    W, H = rect.size
    w, h = t_surf.get_size()
    x = (W - w) / 2
    y = (H - h) / 2
    surf.blit(t_surf, [x, y])

class Button(pygame.sprite.Sprite):
    containers = []
    def __init__(self, image, on_click):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = image
        self.on_click = on_click

class BlockButton(Button):
    def __init__(self, on_click, color, size=(30, 20), pos=(0,0), text=None,
                 font=None, font_color=(255,255,255), font_size=20):
        Button.__init__(self, pygame.Surface(size), on_click)
        self.image.fill(color)
        if text:
            if not font:
                font = pygame.font.Font(None, font_size)
                self.font = font
                self.font_color = font_color
                self.make_text(text)
        self.rect = self.image.get_rect().move(pos)

    def clear_text(self):
        self.image.fill(self.color)
    def make_text(self, text, font_color=None, font=None):
        center_text(text, font or self.font,
                    font_color or self.font_color,
                    self.image.get_rect(),
                    self.image)
