import datingsim, pygame
from textbox import TextBox
from button import BlockButton
from dialogue import CoolDialogue

class DateChoose():

    def __init__(self, font_name=None, desc_font_size=25, desc_font_color=(255,255,255),
                 exit_pos=None, bg_img=None):
        """Select from 6 tiled pictures of locations where a date can take place. \
        Displays gold cost under each tile. Deducts gold and initiates dating sequence when \
        player clicks on a valid tile."""
        self.bg_img = bg_img or None
        self.font_name = font_name
        self.desc_font_size = desc_font_size
        self.desc_font_color = desc_font_color
        self.desc_font = pygame.font.Font(font_name, desc_font_size)

        self.tiles = pygame.sprite.Group()
        tileStartX, tileStartY = 10, 0
        positions = ([[tileStartX + i*Tile.SIZE_X, tileStartY] for i in range(3)] +
            [[tileStartX + i*Tile.SIZE_X, tileStartY + Tile.SIZE_Y] for i in range(3)])
        def make_tile(name, cost, img_key):
            pos = positions.pop(0)
            tile = Tile(name, cost, img_key, pos)
            self.tiles.add(tile)
            def on_click():
                print("You clicked on {}".format(tile.name))
                """Visit this place, if possible. Deduct cash accordingly."""
                if (datingsim.player.inventory.cash >= tile.cost):
                    pass
                else:
                    pass
            def on_hover():
                self.changeText("{} -- cost: {} gold".format(name, cost))
            def on_unhover():
                self.changeText("")
            tile.on_click = on_click
            tile.on_hover = on_hover
            tile.on_unhover = on_unhover
        make_tile("Beach of the East", 500, "TILE_beach_east")
        #make_tile("Beach of the West", 500, "TILE_beach_west")

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.tiles)

        self.main_surface = pygame.display.get_surface()
        self.done = False
        self.curr_tile = None

    def changeText(self, text):
        """render changed text if necessary"""
        print("Text changed to {}.".format(text))

    def main_loop(self):
        while not self.done:
            for e in pygame.event.get():
                if e.type is pygame.QUIT:
                    pygame.quit()
                    datingsim.quit()
                    quit()
                    if e.type is pygame.MOUSEBUTTONDOWN:
                        # detect button collisions here
                        pass
                elif e.type is pygame.MOUSEMOTION:
                    for tile in self.tiles:
                        if tile.rect.collidepoint(e.pos):
                            if (tile != self.curr_tile):
                                tile.on_hover()
                            self.curr_tile = tile
                        elif tile == self.curr_tile: # didn't collide with curr_tile
                            tile.on_unhover()
                            self.curr_tile = None
                elif e.type is pygame.MOUSEBUTTONDOWN:
                    if self.curr_tile != None:
                        self.curr_tile.on_click()

            if self.bg_img:
                self.main_surface.blit(self.bg_img, [0,0])
            self.all_sprites.update()
            self.all_sprites.draw(self.main_surface)
            pygame.display.flip()
            pygame.time.wait(1000//20)
        self.ath()

    def ath(self):
        pass

    @staticmethod
    def test():
        instance = DateChoose()
        instance.main_loop()

class Tile(pygame.sprite.Sprite):
    """Psuedo-button"""
    SIZE_X, SIZE_Y = SIZE = 260, 275
    def __init__(self, name, cost, img_key, pos):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.cost = cost
        self.image = datingsim.assets.get_img_safe(img_key)
        self.rect = pygame.Rect(pos, Tile.SIZE)

if (__name__ == "__main__"):
    pygame.init()
    datingsim.init()
    DateChoose.test()
