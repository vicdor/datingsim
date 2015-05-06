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

        self.buttons = pygame.sprite.Group()
        def finish():
            self.done = True
        self.buttons.add(BlockButton(finish, back_color, back_size, back_pos,
                                     text="Back", font=back_font))
        self.panels = pygame.sprite.Group()

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.buttons, self.all_sprites)

        self.main_surface = pygame.display.get_surface()

    def main_loop(self):
        while not self.done:
            for e in pygame.event.get():
                if e.type is pygame.QUIT:
                    datingsim.quit()
                    pygame.quit()
                    quit()
                elif e.type is pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button.rect.collidepoint(e.pos):
                            button.on_click()
            if self.bg_surf:
                self.main_surface.blit(self.bg_img, (0, 0))
            else:
                self.main_surface.fill((0, 0, 0))
            self.all_sprites.update()
            self.all_sprites.draw(self.main_surface)
            pygame.display.flip()
            pygame.time.wait(1000//20)
        self.ath()

    def ath(self):
        pass

    @staticmethod
    def test():
        InitiateMeet([Isadora(), Kanaya()]).main_loop()

if __name__ == '__main__':
    pygame.init()
    datingsim.init()
    InitiateMeet.test()
