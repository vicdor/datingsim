import pygame, pygame.gfxdraw, pygame.transform
import kitchen
from dreambutton import DreamButton, DreamMap
import datingsim

class MapButton(DreamButton):
    def __init__(self, pos, loc, size=(18,18), color=(255,98,123)):
        def draw(surf, color=color):
            x, y = [int(i) for i in pos]
            rx, ry = [i//2 for i in size]
            pygame.gfxdraw.filled_ellipse(surf, x, y, rx, ry, color)
        def on_click():
            import kitchen
            kitchen.push_scene(loc)
            return True
        DreamButton.__init__(self, draw, on_click)
        self.loc = loc
        self.on_hover = lambda: loc.name

def center_text(text, font, font_color, rect, surf):
    """blits the text into the center of rect on surf"""
    t_surf = font.render(text, False, font_color)
    W, H = rect.size
    w, h = t_surf.get_size()
    x = (W - w) / 2
    y = (H - h) / 2
    surf.blit(t_surf, [x, y])

class WorldMap():
    def __init__(self):
        self.bg_img = datingsim.assets.get_img_safe('BG_island_map')

        self.font = pygame.font.Font(None, 50)
        self.font_color = (125, 200, 128)
        self.name_rect = pygame.Rect(0, datingsim.HEIGHT-100, datingsim.WIDTH, 100)
        self.hover_text = None
        self.main_surface = pygame.display.get_surface()

        self.dream_map = DreamMap()
        self.buttons = []
        button_data = (('club', [187, 408]),
                    ('castle', [665, 213]),
                    ('woods', [185, 355]),
                    ('river', [211, 262]),
                    ('beach_west', [121, 268]),
                    ('beach_east', [575, 360]),
                    ('mountain', [354, 269]),
                    ('springs', [426, 308]),
                    ('gym', [145, 214]),
                    ('valley', [254, 209]),
                    ('inn', [495, 373]),
                    ('village', [353, 194]),
                    ('home', [209, 311]),
                    ('clinic', [531, 225]),
                    ('city', [-20, -20]),
                    ('arcade', [0, 0])
                    )
        for key, pos in button_data:
            loc = datingsim.locs[key]
            m = MapButton(pos, loc)
            self.dream_map.add_dreambutton(m)
            self.buttons.append(m)
        #m = MapButton([50, 50], lambda: print("up next"), "WOWZAAST")
        #buttons.append(m)

    def main_loop(self):
        self.done = False
        while not self.done: # and not kitchen.stop_request:
            for e in pygame.event.get():
                if e.type is pygame.QUIT:
                    kitchen.finish()
                    self.done = True
                elif e.type is pygame.MOUSEBUTTONDOWN:
                    dream = self.dream_map.get_at(e.pos)
                    if dream:
                        click_result = dream.on_click()
                        if click_result:
                            self.done = True
                elif e.type is pygame.MOUSEMOTION:
                    dream = self.dream_map.get_at(e.pos)
                    #print(e.pos, DreamButton.ghost_surf.get_at(pos)[0])
                    if dream:
                        self.hover_text = dream.on_hover()
                    else:
                        self.hover_text = None

            self.main_surface.blit(self.bg_img, [0,0])
            for b in self.buttons:
                b.update()
                b.draw(self.main_surface)
            if self.hover_text:
                center_text(self.hover_text, self.font, self.font_color, self.name_rect,
                            self.main_surface)
            pygame.time.wait(1000//15)
            pygame.display.flip()
        self.ath()

    def ath(self):
        pass

    @staticmethod
    def test():
        pygame.init()
        datingsim.init()
        pygame.display.set_caption("World Map")
        GAME_SIZE = GAME_WIDTH, GAME_HEIGHT = datingsim.RESOLUTION
        datingsim.player.inventory.cash = 1000
        instance = WorldMap()
        instance.main_loop()

if __name__ == '__main__':
    WorldMap.test()
