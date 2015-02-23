import datingsim, pygame
from button import BlockButton
from gurl import Gurl

class MeetScene:

    def __init__(self, gurl):
        self.gurl = gurl
        self.meet_advisor = MeetAdvisor(gurl)

        self.buttons = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.meet_advisor,
                                self.gurl_textbox)

    def ath(self):
        for s in self.all_sprites:
            s.kill()

    def update_conversation(self, text):
        self.gurl_textbox.text = text;
        # render new text?


class MeetAdvisor(pygame.sprite.Sprite):
    def __init__(self, gurl, pos=(600, 20), font_color=(200,50,60),
                 font_size=20, font_file=None
                 ):
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
    MeetAdvisor.test_text()




