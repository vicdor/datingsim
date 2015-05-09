import datingsim, pygame
from textbox import TextBox
from button import BlockButton
from dialogue import CoolDialogue

class DateScene():

    def __init__(self, gurl, bg_img=None, font_name):
        Scene.__init__(self)
        self.bg_img = bg_img or None
        self.font_name = font_name

        self.show_menu_buttons = True
        self.gurl = gurl
        self.gurl_sprite = gurl.get_default_img

    def main_loop(self):
        self.all_sprites.empty()
        self.buttons.empty()

        self.all_sprites.add(self.gurl_sprite)

        if self.show_menu_buttons:
            self.all_sprites.add(self.menu_buttons)
            self.buttons.add(self.menu_buttons)
        Scene.main_loop(self)

