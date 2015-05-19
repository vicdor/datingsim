import datingsim, pygame
import random
from textbox import TextBox
from button import BlockButton
from dialogue import CoolDialogue
from scene import Scene

class DateScene(Scene):

    def __init__(self, gurl, bg_img=None, font_name=None, gurl_img_pos=(100,100),
                 gurl_talk_pos=(20, 100), gurl_talk_size=(500, 230),
                 gurl_talk_color=(180,70,70), gurl_talk_font_color=(255,255,255)
                 ):
        Scene.__init__(self)
        self.bg_img = bg_img
        self.font_name = font_name

        self.show_menu_buttons = True
        self.show_heart_meter = True
        self.show_gurl_textbox = False
        self.show_quiz_buttons = True

        self.remaining_trivia_keys = gurl.get_randomized_trivia_keys()

        self.gurl = gurl

        self.gurl_img_pos = gurl_img_pos
        self.mood = "default"

        self.heart_meter = HeartMeter()

        self.gurl_textbox = TextBox("gurl talk filler", gurl_talk_pos, gurl_talk_size,
            font=None, bg_color=gurl_talk_color, font_color=gurl_talk_font_color)

        self.menu_buttons = pygame.sprite.Group()
        menu_x, menu_y = 10, 480
        def make_menu_button(name, on_click, size=(110, 50),
                        spacing=(20, 0), color=(140,60,60)):
            nonlocal menu_x, menu_y
            menu_x = menu_x + size[0] + spacing[0]
            menu_y = menu_y + spacing[1]
            pos = (menu_x, menu_y)
            button = BlockButton(on_click, color, size, pos, name,
                self.font_name)
            self.menu_buttons.add(button)
        make_menu_button("talk", self.select_talk)
        make_menu_button("compliment", self.select_compliment)
        make_menu_button("gift", self.select_gift)
        make_menu_button("photo", self.select_photo)
        make_menu_button("kiss", self.select_kiss)

        self.quiz_buttons = pygame.sprite.Group()
        quiz_start_pos = (10, 280)
        quiz_size = (280, 70)
        quiz_spacing = (15, 15)
        quiz_posses = [quiz_start_pos,
            (quiz_start_pos[0]+quiz_size[0]+quiz_spacing[0], quiz_start_pos[1]),
            (quiz_start_pos[0], quiz_start_pos[1]+quiz_size[1]+quiz_spacing[1]),
            (quiz_start_pos[0]+quiz_size[0]+quiz_spacing[0],
             quiz_start_pos[1]+quiz_size[1]+quiz_spacing[1])
        ]
        def make_quiz_button(name, on_click, size=quiz_size, color=(140,60,60)):
            pos = quiz_posses.pop(0)
            button = BlockButton(on_click, color, size, pos, name, self.font_name)
            self.quiz_buttons.add(button)
        make_quiz_button("Hello there", self.select_quiz_A)
        make_quiz_button("100 cm", None)
        make_quiz_button("20 cm", None)
        make_quiz_button("10 cm", None)

        self.update_heart_meter(10)
        self.open_quiz()

    def open_quiz(self, key=None):
        key = key or self.remaining_trivia_keys.pop(0)
        question = self.gurl.quiz_questions[key]
        answer = self.gurl.trivia[key]
        spoofs = self.gurl.spoofs[key][:]
        index_correct = random.randint(0, 3)
        print(key, question, answer, spoofs, index_correct)
        def choose_faulty():
            print("wrong!")
        def choose_correct():
            print("correct!")
        for i, button in enumerate(self.quiz_buttons):
            if i == index_correct:
                text = answer
                button.on_click = choose_correct
            else:
                text = spoofs.pop(0)
                button.on_click = choose_faulty
            button.make_text(str(text))

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

    def select_quiz_A(self):
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

    def update_heart_meter(self, percentage):
        self.percentage = percentage
        self.heart_meter.textbox.text = "{}%".format(percentage)
        self.heart_meter.textbox.render()
        print("ba-dump! {}%".format(percentage))

    def main_loop(self):
        self.all_sprites.empty()
        self.buttons.empty()

        #self.all_sprites.add(self.gurl_sprite)

        if self.show_menu_buttons:
            self.all_sprites.add(self.menu_buttons)
            self.buttons.add(self.menu_buttons)

        if self.show_heart_meter:
            self.all_sprites.add(self.heart_meter)

        if self.show_gurl_textbox:
            self.all_sprites.add(self.gurl_textbox)

        if self.show_quiz_buttons:
            self.all_sprites.add(self.quiz_buttons)
            self.buttons.add(self.quiz_buttons)

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

class HeartMeter(pygame.sprite.Sprite):
    def __init__(self, pos=(30,30), size=(100,40), bg_color=(234,34,60), text_pos=0):
        pygame.sprite.Sprite.__init__(self)
        self.bg_color = bg_color
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect().move(pos)
        self.textbox = TextBox("__%", (0, 0), size)
        self.update()

    def update(self):
        self.image.fill(self.bg_color)
        self.image.blit(self.textbox.image, (0, 0))

if __name__ == "__main__":
    DateScene.test()

