import datingsim, pygame

class Scene():

    def __init__(self):
        self.buttons = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.bg_surf = None
        self.done = False
        self.main_surface = pygame.display.get_surface()

    def main_loop(self):
        while not self.done:
            self.main_loop_before()
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
                self.main_surface.blit(self.bg_surf, (0, 0))
            else:
                self.main_surface.fill((0, 0, 0))
            self.all_sprites.update()
            self.all_sprites.draw(self.main_surface)
            pygame.display.flip()
            self.main_loop_after()
            pygame.time.wait(1000//20)
        self.ath()

    def main_loop_before(self):
        """Overide this method to add behavior at start of loop."""
        pass

    def main_loop_after(self):
        """Overide this method to add behavior at end of loop.
           Runs after draw and before delay."""
        pass

    def ath(self):
        pass

    @staticmethod
    def test():
        pygame.init()
        datingsim.init()
        Scene().main_loop()

if __name__ == '__main__':
    pygame.init()
    datingsim.init()
    Scene.test()
