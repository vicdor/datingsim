import datingsim, pygame
from textbox import TextBox
from button import BlockButton
from dialogue import CoolDialogue
from scene import Scene

class DateScene(Scene):

    def __init__(self, gurl, bg_img=None, font_name=None,
                 gurl_img_pos=(100,100)):
        Scene.__init__(self)
        self.bg_img = bg_img
        self.font_name = font_name

        self.show_menu_buttons = True
        self.gurl = gurl
        self.gurl_img_pos = gurl_img_pos
        self.mood = "default"

        self.menu_buttons = pygame.sprite.Group()
        menu_x, menu_y = 10, 480
        def make_button(name, on_click, size=(110, 50),
                        spacing=(20, 0), color=(140,60,60)):
            nonlocal menu_x, menu_y
            menu_x = menu_x + size[0] + spacing[0]
            menu_y = menu_y + spacing[1]
            pos = (menu_x, menu_y)
            button = BlockButton(on_click, color, size, pos, name,
                self.font_name)
            self.menu_buttons.add(button)
        make_button("talk", self.select_talk)
        make_button("compliment", self.select_compliment)
        make_button("gift", self.select_gift)
        make_button("photo", self.select_photo)
        make_button("kiss", self.select_kiss)

    def select_talk(self):
        pass

    def select_compliment(self):
        pass

    def select_gift(self):
        pass

    def select_photo(self):
        pass

    def select_kiss(self):
        pass

    def get_gurl_img(self):
        if self.mood in self.gurl.img_dict:
            return self.gurl.img_dict[self.mood]
        elif 'default' in self.gurl.img_dict:
            return self.gurl.img_dict['default']
        else:
            # just return any image
            for img in self.gurl.img_dict.values():
                return img

    def change_mood(self, new_mood):
        if new_mood in self.gurl.img_dict:
            self.mood = new_mood

    def update_conversation(self, text):
        self.gurl_textbox.text = text;
        self.gurl_textbox.render()


    def main_loop(self):
        self.all_sprites.empty()
        self.buttons.empty()

        #self.all_sprites.add(self.gurl_sprite)

        if self.show_menu_buttons:
            self.all_sprites.add(self.menu_buttons)
            self.buttons.add(self.menu_buttons)

        self.main_surface.blit(self.get_gurl_img(), self.gurl_img_pos)

        while not self.done:
            for event in pygame.event.get():
                if event.type is pygame.QUIT:
                    datingsim.quit()
                    pygame.quit()
                    return
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
    def test():
        from gurl import Isadora
        pygame.init()
        datingsim.init()
        instance = DateScene(Isadora())
        instance.main_loop()

if __name__ == "__main__":
    DateScene.test()

