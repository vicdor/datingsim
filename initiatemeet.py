import datingsim, pygame
from button import BlockButton
from gurl import Isadora, Kanaya
from scene import Scene

class InitiateMeet(Scene):

    def __init__(self, gurls, bg_surf=None, back_color=(234,45,30), back_pos=(40,500),
                 back_size=(70,40), back_font=None):
        Scene.__init__(self)
        self.gurls = gurls  # expect three
        self.bg_surf = bg_surf
        self.done = False

        def finish():
            self.done = True
        self.buttons.add(BlockButton(finish, back_color, back_size, back_pos,
                                     text="Back", font=back_font))
        self.gurl_sprites = pygame.sprite.Group()
        gurl_pos = [(100, 100), (300, 100), (500, 100)]

        def make_gurl_sprite(gurl):
            pos = gurl_pos.pop(0)
            sprite = GurlSprite(gurl, pos)
            self.gurl_sprites.add(sprite)

        make_gurl_sprite(Kanaya())
        make_gurl_sprite(Isadora())

        self.all_sprites.add(self.buttons, self.gurl_sprites)
        self.main_surface = pygame.display.get_surface()

    @staticmethod
    def test():
        InitiateMeet([Isadora(), Kanaya()]).main_loop()

class GurlSprite(pygame.sprite.Sprite):

    def __init__(self, gurl, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = gurl.default_img().copy()
        self.rect = self.image.get_rect().move(pos)

if __name__ == '__main__':
    pygame.init()
    datingsim.init()
    InitiateMeet.test()
