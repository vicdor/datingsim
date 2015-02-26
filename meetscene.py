import datingsim, pygame
from button import BlockButton
from textbox import TextBox
from gurl import Gurl

class MeetScene:

    def __init__(self, gurl, bg_img=None, gurl_img_pos=(300, 300),
                 textPos=(0,400), textSize=(130,180)):
        self.gurl = gurl
        self.bg_img = bg_img
        self.gurl_img_pos = gurl_img_pos
        self.meet_advisor = MeetAdvisor(gurl)

        self.buttons = pygame.sprite.Group()
        prevx, prevy = None, 300
        def make_button(name, on_click, size=(110, 50), color=(140,60,60),
                        dx=20):
            nonlocal prevx
            if prevx == None:
                x = dx
            else:
                x = prevx + dx + size[0]
            y = prevy
            b = BlockButton(on_click, color, pos=(x,y), size=size, text=name)
            prevx = x
            self.buttons.add(b)
        make_button("test button", lambda: print("test 1"))
        def finish():
            self.done = True
        make_button("end", finish)
        make_button("update conv", lambda: self.update_conversation("changed"))

        self.gurl_textbox = TextBox("filler", textPos, textSize)
        self.all_sprites = pygame.sprite.Group(self.meet_advisor,
                            self.gurl_textbox, self.buttons)
        self.done = False;
        self.main_surface = pygame.display.get_surface()

    def ath(self):
        for s in self.all_sprites:
            s.kill()

    def get_gurl_img(self):
        for img in self.gurl.img_dict.values():
            return img

    def update_conversation(self, text):
        self.gurl_textbox.text = text;
        self.gurl_textbox.render()


    def main_loop(self):

        while not self.done:
            for event in pygame.event.get():
                if event.type is pygame.QUIT:
                    self.done = True
                    # datingsim.quit()
                    # pygame.quit()
                # implement button fade on mouse hover
                # make this part of button class default??
                elif event.type is pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button.rect.collidepoint(event.pos):
                            button.on_click()

            if self.bg_img:
                self.main_surface.blit(self.bg_img, (0, 0))
            else:
                self.main_surface.fill((0, 0, 0))
            self.main_surface.blit(self.get_gurl_img(), self.gurl_img_pos)

            self.all_sprites.update()
            self.all_sprites.draw(self.main_surface)
            pygame.display.flip()
            pygame.time.wait(1000//20)



    @staticmethod
    def test_instantiate():
        pygame.init()
        datingsim.init()
        gurl = Gurl("Rudy", None, None)
        gurl.exp = 2000
        d = MeetScene(gurl)

    @staticmethod
    def test_run():
        pygame.init()
        datingsim.init()
        gurl_imgs = {}
        gurl_imgs['askance'] = datingsim.assets.get_img_safe('GURL_kanaya_askance')
        gurl = Gurl("Rudy", gurl_imgs, None)
        gurl.exp = 2000
        d = MeetScene(gurl)
        d.main_loop()
        d.ath()



class MeetAdvisor(pygame.sprite.Sprite):
    def __init__(self, gurl, pos=(600, 20), font_color=(200,50,60),
                 font_size=20, font_file=None
                 ):
        pygame.sprite.Sprite.__init__(self)
        self.gurl = gurl
        self.pos = pos
        self.font_color = font_color
        self.font = pygame.font.Font(font_file, font_size)
        self.update()

    def update(self):
        exp = self.gurl.exp
        rel_name = self.gurl.calc_rel_level()
        self.text = ("Gurl: {} exp:{} lvl:{}"
                ).format(self.gurl.name, exp, rel_name)
        self.image = self.font.render(self.text, False, self.font_color)
        self.rect = self.image.get_rect().move(self.pos)

    # TODO: center rectangle at bottom of screen?

    @staticmethod
    def test_text():
        pygame.init()
        datingsim.init()
        gurl = Gurl("Rudy", None, None)
        gurl.exp = 2000
        m = MeetAdvisor(gurl)
        print(m.text)

if __name__ == "__main__":
    #MeetAdvisor.test_text()
    #MeetScene.test_instantiate()
    MeetScene.test_run()




