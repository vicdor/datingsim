import pygame
from textbox import TextBox
from button import BlockButton

class Dialogue:

    debug = False

    def __init__(self, text, popup_pos, popup_bg_surf, text_box_pos, text_box_size,
                 okay_pos, okay_size, okay_color=(120,230,120),
                 okay_font_color=(255,255,255), font=None, font_size=25,
                 font_color=(255,255,255), snapshot=None,
                 text_box_bg_color=None, **text_box_style):
        self.text = text
        self.popup_pos = popup_pos
        self.popup_bg_surf = popup_bg_surf
        self.popup_surf = pygame.Surface(popup_bg_surf.get_rect().size)
        self.done = False
        def on_click():
            self.done = True
        self.okay_btn = BlockButton(on_click, okay_color, okay_size, okay_pos,
                                    text="okay", font_color=okay_font_color)
        self.text_box = TextBox(text, text_box_pos, text_box_size, font=font,
                                font_color=font_color, font_size=font_size,
                                bg_color=text_box_bg_color,
                                **text_box_style)
        self.snapshot = snapshot
        self.main_surface = pygame.display.get_surface()
        self.popup_group = pygame.sprite.Group(self.okay_btn, self.text_box)

    def ath(self):
        self.okay_btn.kill()
        self.text_box.kill()

    def main_loop(self):
        while not self.done:
            for e in pygame.event.get():
                if e.type is pygame.QUIT:
                    pygame.quit()
                    quit()
                if e.type is pygame.MOUSEBUTTONDOWN:
                    rect = self.okay_btn.rect.move(self.popup_pos)
                    if rect.collidepoint(e.pos):
                        self.okay_btn.on_click()
            if self.snapshot:
                self.main_surface.blit(self.snapshot, [0,0])
            self.popup_surf.blit(self.popup_bg_surf, [0,0])
            self.popup_group.update()
            self.popup_group.draw(self.popup_surf)
            self.main_surface.blit(self.popup_surf, self.popup_pos)
            pygame.display.flip()
            pygame.time.wait(1000//20)
        self.ath()

    @staticmethod
    def test():
        pygame.init()
        pygame.display.set_caption("Dialogue")
        GAME_SIZE = GAME_WIDTH, GAME_HEIGHT = (800, 600)
        screen = pygame.display.set_mode(GAME_SIZE)

        popup_w, popup_h = popup_size = (400,300)
        popup_bg_surf = pygame.Surface(popup_size)
        popup_bg_surf.fill([10,60,80])
        popup_pos = (GAME_WIDTH - popup_w)/2, (GAME_HEIGHT - popup_h)/2
        text_box_w, text_box_h = text_box_size = (370, 200)
        text_box_pos = (popup_w - text_box_w)/2, (popup_h - text_box_h)/2
        text = ("Lorem ipsum lumpus rumpus fruity patootie. In the beginning "
            "there was dark. What is?")
        okay_w, okay_h = okay_size = (80, 50)
        okay_pos = (popup_w - okay_w)/2, (popup_h - okay_h - 3)
        snapshot = pygame.image.load('new-zealand.jpg').convert()

        d = Dialogue(text, popup_pos, popup_bg_surf, text_box_pos, text_box_size,
                     okay_pos, okay_size, snapshot=snapshot)
        d.main_loop()
        pygame.quit()

class CoolDialogue(Dialogue):

    def __init__(self, text, snapshot=None):
        GAME_WIDTH, GAME_HEIGHT = GAME_SIZE = pygame.display.get_surface().get_size()
        popup_w, popup_h = popup_size = (400,300)
        popup_bg_color = (10, 60, 80)
        popup_bg_surf = pygame.Surface(popup_size)
        popup_bg_surf.fill(popup_bg_color)
        popup_pos = (GAME_WIDTH - popup_w)/2, (GAME_HEIGHT - popup_h)/2
        text_box_w, text_box_h = text_box_size = (370, 200)
        text_box_pos = (popup_w - text_box_w)/2, (popup_h - text_box_h)/2
        text_box_bg_color = (0, 0, 0)
        okay_w, okay_h = okay_size = (80, 50)
        okay_pos = (popup_w - okay_w)/2, (popup_h - okay_h - 3)

        Dialogue.__init__(self, text, popup_pos, popup_bg_surf, text_box_pos, text_box_size,
                 okay_pos, okay_size,
                 text_box_bg_color=text_box_bg_color, snapshot=snapshot)

    @staticmethod
    def test():
        pygame.init()
        pygame.display.set_caption('CoolDialogue')
        GAME_WIDTH, GAME_HEIGHT = GAME_SIZE = (600, 400)
        screen = pygame.display.set_mode(GAME_SIZE)
        text = ("Lorem ipsum lumpus rumpus fruity patootie. In the beginning "
            "there was dark. What is?")
        c = CoolDialogue(text)
        c.main_loop()
        pygame.quit()

if __name__ == '__main__':
    Dialogue.test()
    CoolDialogue.test()







