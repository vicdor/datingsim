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
        self.panels = pygame.sprite.Group()

        self.all_sprites.add(self.buttons, self.panels)
        self.main_surface = pygame.display.get_surface()

    @staticmethod
    def test():
        InitiateMeet([Isadora(), Kanaya()]).main_loop()

if __name__ == '__main__':
    pygame.init()
    datingsim.init()
    InitiateMeet.test()
