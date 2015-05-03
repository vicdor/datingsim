import pygame
if __name__ != '__main__':
    import datingsim

def do_force_fit(img):
    if __name__ == '__main__':
        RESOLUTION = pygame.display.get_surface().get_size()
    else:
        RESOLUTION = datingsim.RESOLUTION
    return pygame.transform.scale(img, RESOLUTION)

class Assets():
    use_fillers = True
    filler_color = (50, 50, 50)
    instance = None

    imgs = {}
    msks = {}

    def __init__(self):
        self._dict = {}
        self.load_all()

    def load_all(self):
        imgs = Assets.imgs
        images = [('NZ_map', 'new-zealand-map.jpg', True),
                  ('BG_beach_east', 'beach.jpg', True),
                  ('BG_island_map', 'island-map.jpg', True),
                  ('BG_river', 'river.jpg', True),
                  ('BG_club', 'club.jpg', True),

                  ('GURL_kanaya_askance', 'kanaya_askance.png', False),
                  ('GURL_kanaya_smile', 'kanaya_smile.png', False),
                  ('GURL_isadora_default', 'isadora_default.jpg', False),

                  ('TILE_beach_east', 'beachicon1.jpg', False)
                ]
        for key, file_name, force_fit in images:
            img = pygame.image.load('assets/'+file_name).convert()
            if force_fit and __name__ != '__main__':
                img = do_force_fit(img)
            self.imgs[key] = img

        msk_data = [('club', 'club.wav'),
                ('forest', 'forest.wav')

                ]
        for key, file_name in msk_data:
            Assets.msk = pygame.mixer.Sound('assets/' + file_name)
            self.msks[key] = file_name

    #quick hack for use_fillers
    def get_img_safe(self, item):
        imgs = Assets.imgs
        if item not in imgs and self.use_fillers:
            filler = FillerArt(item, color=Assets.filler_color)
            if item.startswith('BG') and __name__ != '__main__':
                filler = do_force_fit(filler)
            imgs[item] = filler
        return imgs[item]

    get_img = get_img_safe

    '''
    def get(self, item):
        if self.use_fillers and item not in self._dict:
            self._dict[item] = FillerArt(item, color=Assets.filler_color)
        return self._dict[item]

    def __getitem__(self, item):
        return self.get(item)
    '''

class FillerArt(pygame.Surface):

    def __init__(self, name, size=(100,100), color=(100,200,110),
                 font=None, font_size=20, font_color=(255,255,255)):
        pygame.Surface.__init__(self, size)
        self.fill(color)
        font = font or pygame.font.Font(None, font_size)
        text_surf = font.render(name, False, font_color)
        text_w, text_h = text_surf.get_size()
        w, h = size
        text_pos = text_x, text_y = (w-text_w)/2, (h-text_h)/2
        self.blit(text_surf, text_pos)

    def test():
        RESOLUTION = WIDTH, HEIGHT = 800, 600
        pygame.init()
        pygame.display.set_caption("FillerArt")
        screen = pygame.display.set_mode(RESOLUTION)
        things = [("ironic", 20, 5), ("moronic", 200, 400)]
        for name, x, y in things:
            filler = FillerArt(name)
            screen.blit(filler, [x,y])

        assets = Assets()
        assets.use_fillers = True
        filler = assets.get_img_safe("not in Assets")
        screen.blit(filler, [70,8])
        pygame.display.flip()

        done = False
        while not done:
            for e in pygame.event.get():
                if e.type is pygame.QUIT:
                    done = True
            pygame.time.wait(1000//20)
        pygame.quit()

if __name__ == '__main__':
    FillerArt.test()

