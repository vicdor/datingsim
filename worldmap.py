import pygame, pygame.gfxdraw, pygame.transform
from dreambutton import DreamButton
import datingsim

class MapButton(DreamButton):
    def __init__(self, pos, loc, size=(18,18), color=(255,98,123)):
        def draw(surf, color=color):
            x, y = [int(i) for i in pos]
            rx, ry = [i//2 for i in size]
            pygame.gfxdraw.filled_ellipse(surf, x, y, rx, ry, color)
        DreamButton.__init__(self, draw, loc.enter)
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

pygame.init()
datingsim.init()
pygame.display.set_caption("World Map")
screen = pygame.display.get_surface()
GAME_SIZE = GAME_WIDTH, GAME_HEIGHT = datingsim.RESOLUTION
def world_map():
    bg_img = datingsim.assets.get_img_safe('BG_island_map')

    font = pygame.font.Font(None, 50)
    font_color = (125, 200, 128)
    name_rect = pygame.Rect(0, GAME_HEIGHT-100, GAME_WIDTH, 100)
    hover_text = None


    DreamButton.reset()
    buttons = []
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
                   ('clinic', [531, 225]),
                   ('city', [-20, -20])
                   )
    for key, pos in button_data:
        loc = datingsim.locs[key]
        m = MapButton(pos, loc)
        buttons.append(m)
    #m = MapButton([50, 50], lambda: print("up next"), "WOWZAAST")
    #buttons.append(m)

    done = False
    while not done:
        for e in pygame.event.get():
            if e.type is pygame.QUIT:
                done = True
            elif e.type is pygame.MOUSEBUTTONDOWN:
                dream = DreamButton.get_at(e.pos)
                print(e.pos)
                if dream:
                    click_result = dream.on_click()
                    if click_result:
                        done = True
            elif e.type is pygame.MOUSEMOTION:
                dream = DreamButton.get_at(e.pos)
                #print(e.pos, DreamButton.ghost_surf.get_at(pos)[0])
                if dream:
                    hover_text = dream.on_hover()
                else:
                    hover_text = None

        screen.blit(bg_img, [0,0])
        for b in buttons:
            b.update()
            b.draw(screen)
        if hover_text:
            center_text(hover_text, font, font_color, name_rect, screen)
        pygame.time.wait(1000//15)
        pygame.display.flip()

world_map()





