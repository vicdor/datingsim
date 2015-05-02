import datingsim, pygame
from textbox import TextBox
from button import BlockButton
from dialogue import CoolDialogue

class ShopDialogue():

    def __init__(self, popup_pos, items, popup_size=None, popup_bg_surf=None,
                 items_spacing1=15, items_spacing2=15, item_y=10,
                 text_box_y = 10, font=None, font_color=(1,70,10),
                 font_size=20, slot_height=None, cash_slot_height=50,
                 exit_btn_color=(2,2,80), exit_btn_size=(70,45),
                 exit_btn_spacing=(5,5), exit_btn_text="Exit",
                 exit_btn_font_color=(70,70,70),
                 main_surface=None, snapshot=None):
        # TODO: exit_btn and shop title
        self.popup_pos = popup_pos
        self.items = items
        self.popup_bg_surf = popup_bg_surf
        if popup_bg_surf:
            self.popup_size = popup_bg_surf.get_size()
        else:
            self.popup_size = popup_size

        self.popup_surf = pygame.Surface(self.popup_size)
        self.items_spacing1 = items_spacing1
        self.items_spacing2 = items_spacing2
        self.item_y = item_y
        self.text_box_y = text_box_y
        self.font = font or pygame.font.Font(None, font_size)
        self.font_color = font_color

        # spacing is relative to right-bottom of dialogue. make negative so
        # relevant rectangle can be moved up.
        exit_btn_pos = [self.popup_size[i] -exit_btn_size[i]-exit_btn_spacing[i]
                        for i in range(2)]
        def exit_on_click():
            self.done = True
        self.exit_btn = BlockButton(exit_on_click, exit_btn_color,
                                    size=exit_btn_size, pos=exit_btn_pos,
                                    text=exit_btn_text,
                                    font_color=exit_btn_font_color)
        self.slot_height = (slot_height or
                (self.popup_size[1] - cash_slot_height) // 3)
        # self.slot_surfs = [
        #     self.popup_surf.subsurface(pygame.Rect(
        #         left=0, top=self.slot_height*i,
        #         width=self.popup_size[0], height=self.slot_height),
        #     )
        #     for i in range(3)
        # ]
        self.slot_surfs = [None] * 3
        self.slot_surf_rects = [None] * 3
        for i in range(3):
            self.slot_surf_rects[i] = pygame.Rect(
                        0, self.slot_height*i,
                        self.popup_size[0], self.slot_height)
            self.slot_surfs[i] = (
                self.popup_surf.subsurface(self.slot_surf_rects[i])
            )
        '''Doesn't work because pygame.Surface attributes are locked :P'''
        #for slot_surf in self.slot_surfs:
        #    def on_hover():
        #        slot_surf.set_alpha(255)
        #    def on_unhover():
        #        slot_surf.set_alpha(200)
        #    slot_surf.on_hover = on_hover
        #    slot_surf.on_unhover = on_unhover
        self.slot_text_boxs = [None] * 3
        self.main_surface = main_surface or pygame.display.get_surface()
        self.snapshot = snapshot

    def render_slot(self, n):
        slot_surf = self.slot_surfs[n]
        item = self.items[n]

        pic_pos = (self.items_spacing1, self.item_y)
        slot_surf.blit(item.pic, pic_pos)

        if not self.slot_text_boxs[n]:
            pic_w = item.pic.get_size()[0]
            x = (self.items_spacing1 + self.items_spacing2 +
                pic_w)
            y = self.text_box_y
            pos = x, y
            size = (self.popup_surf.get_size()[0] - x,
                    self.popup_surf.get_size()[1])
            self.slot_text_boxs[n] = TextBox('filler', pos,
                size=size, font=self.font, font_color=self.font_color)

        inv = datingsim.player.inventory
        text = ("{name}\n${cost}    Already own: {owned}"
                ).format(name=item.name, cost=item.cost,
                         owned=item.quantity)
        t = self.slot_text_boxs[n]
        t.text = text
        t.render()
        slot_surf.blit(t.image, t.rect.topleft)

    def get_slot_rect(self, n):
        '''gets slot_rect relative to popup surface'''
        pos = (0, 0)
        h_displace = 0, self.slot_height * n
        return self.slot_surfs[n].get_rect().move(pos).move(h_displace)

    def on_click_slot(self, n):
        #print("slot {} was clicked.".format(n))
        item = self.items[n]
        p = datingsim.player
        inv = p.inventory
        if inv.can_buy(item):
            inv.buy(item)
            self.buy_success(item)
        else:
            self.buy_fail(item)

    def buy_success(self, item):
        CoolDialogue("Successfully purchased {}.".format(item.name)).main_loop()

    def buy_fail(self, item):
        text = ("Not enough money to purchase {}."
                ).format(item.name)
        CoolDialogue(text).main_loop()


    def ath(self):
        for t in self.slot_text_boxs:
            if t:
                t.kill()
        self.exit_btn.kill()


    def main_loop(self, auto_ath=True):
        self.done = False
        md = lambda x: x #and hasattr(x, 'on_click')
        mu = lambda x: x #and hasattr(x, 'on_hover')
        mousedowns = list(filter(md, self.slot_surfs))
        mouseups = list(filter(mu, self.slot_surfs))

        while not self.done:
            curr_mouse_pos = None
            for e in pygame.event.get():
                if e.type is pygame.QUIT:
                    self.done = True
                if e.type is pygame.MOUSEBUTTONDOWN:
                    pos = self.convert_pos(e.pos)
                    if self.exit_btn.rect.collidepoint(pos):
                        self.exit_btn.on_click()
                    for i, b in enumerate(mousedowns):
                        rect = self.get_slot_rect(i)
                        if rect.collidepoint(pos):
                            self.on_click_slot(i)
                #if e.type is pygame.MOUSEMOTION:
                #    curr_mouse_pos = pos = self.convert_pos(e.pos)
                #    for b in mouseups:
                #        if b.rect.collidepoint(pos):
                #            b.on_hover()
                #        else:
                #            if hasattr(b, 'on_unhover'):
                #                b.on_unhover()

            if self.snapshot:
                self.main_surface.blit(self.snapshot, [0,0])

            self.popup_surf.blit(self.popup_bg_surf, [0,0])

            for n in range(len(self.items)):
                self.render_slot(n)

            self.popup_surf.blit(self.exit_btn.image,
                                 self.exit_btn.rect.topleft)
            self.main_surface.blit(self.popup_surf, self.popup_pos)




            pygame.display.flip()
            pygame.time.wait(1000//20)

        if auto_ath:
            self.ath()

    def convert_pos(self, pos):
        '''converts from main surface coordinates to popup_surf coordinates'''
        return [pos[i] - self.popup_pos[i] for i in range(2)]

    @staticmethod
    def test():
        pygame.init()
        datingsim.init()
        pygame.display.set_caption("Shop test")

        W, H = datingsim.RESOLUTION
        popup_w, popup_h = popup_size = (400, 600)
        popup_x, popup_y = popup_pos = (
            (W - popup_w) / 2,
            (H - popup_h) / 2
        )
        popup_bg_color = (255, 255, 255)
        popup_bg_surf = pygame.Surface(popup_size)
        popup_bg_surf.fill(popup_bg_color)
        items = [datingsim.player.inventory.get(key)
                 for key in ('potion', 'arrows', 'tractor')]

        shop = ShopDialogue(popup_pos, items, popup_bg_surf=popup_bg_surf)
        shop.main_loop()

        datingsim.quit()
        pygame.quit()

class CoolShop(ShopDialogue):
    def __init__(self, items):
        W, H = datingsim.RESOLUTION
        popup_w, popup_h = popup_size = (400, 600)
        popup_x, popup_y = popup_pos = (
            (W - popup_w) / 2,
            (H - popup_h) / 2
        )
        popup_bg_color = (255, 255, 255)
        popup_bg_surf = pygame.Surface(popup_size)
        popup_bg_surf.fill(popup_bg_color)

        ShopDialogue.__init__(self, popup_pos, items,
                              popup_bg_surf=popup_bg_surf)

class GiveDialogue(CoolShop):
    def __init__(self, items):
        CoolShop.__init__(self, items)
        self.item = None

    def on_click_slot(self, n):
        #print("slot {} was clicked.".format(n))
        item = self.items[n]
        p = datingsim.player
        inv = p.inventory
        if inv.can_rid(item):
            inv.rid(item)
            self.rid_success(item)
        else:
            self.rid_fail(item)
    def rid_success(self, item):
        """Okay, i'm sort of proud of this one"""
        self.done = True
        self.item = item
        CoolDialogue("You gave an {}.".format(item.name)).main_loop();
    def rid_fail(self, item):
        CoolDialogue("You don't own an {}!".format(item.name)).main_loop();



if __name__ == '__main__':
    ShopDialogue.test()



