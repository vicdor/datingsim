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
            for e in pygame.event.get():
                if e.type is pygame.QUIT:
                    datingsim.quit()
                    pygame.quit()
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
            pygame.time.wait(1000//20)
        self.ath()

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
