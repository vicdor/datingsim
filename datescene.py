import datingsim, pygame
import random
from textbox import TextBox
from button import BlockButton
from dialogue import CoolDialogue
from scene import Scene
from shop import GiveDialogue

class DateScene(Scene):

    def __init__(self, gurl, init_hearts=10, bg_img=None, font=None, gurl_img_pos=(100,100),
                 gurl_talk_pos=(20, 100), gurl_talk_size=(500, 130),
                 gurl_talk_color=(180,70,70), gurl_talk_font_color=(255,255,255)
                 ):
        Scene.__init__(self)
        self.bg_img = bg_img
        self.font = font or datingsim.assets.get_default_font()

        self.show_menu_buttons = True
        self.show_heart_meter = True
        self.show_gurl_textbox = True
        self.show_quiz_buttons = False

        self.remaining_trivia_keys = gurl.get_randomized_trivia_keys()
        self.compliment_count = 0
        self.gift_count = 0
        self.photo_count = 0
        self.fail_kiss_count = 0

        self.gurl = gurl
        self.gurl_img_pos = gurl_img_pos
        self.mood = "default"
        self.heart_meter = HeartMeter()
        self.update_heart_meter(init_hearts)

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
                self.font)
            self.menu_buttons.add(button)
        make_menu_button("talk", self.select_talk)
        make_menu_button("compliment", self.select_compliment)
        make_menu_button("gift", self.select_gift)
        make_menu_button("photo", self.select_photo)
        make_menu_button("kiss", self.select_kiss)

        self.back_button = BlockButton(self.select_back, datingsim.COLOR_D, (110, 50),
                    (400,300), "Back", self.font)


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
            button = BlockButton(on_click, color, size, pos, name, self.font)
            self.quiz_buttons.add(button)
        make_quiz_button("filler A", None)
        make_quiz_button("filler B", None)
        make_quiz_button("filler C", None)
        make_quiz_button("filler D", None)

    def open_quiz(self, key=None):
        self.show_quiz_buttons = True
        self.show_menu_buttons = False
        self.show_gurl_textbox = True
        self.show_heart_meter = True
        key = key or self.remaining_trivia_keys.pop(0)
        question = self.gurl.quiz_questions[key]
        answer = self.gurl.trivia[key]
        spoofs = self.gurl.spoofs[key][:]
        index_correct = random.randint(0, 3)
        self.update_conversation(question)
        for i, button in enumerate(self.quiz_buttons):
            if i == index_correct:
                text = answer
                button.on_click = self.on_correct_answer
            else:
                text = spoofs.pop(0)
                button.on_click = self.on_wrong_answer
            button.make_text(str(text))

    def on_correct_answer(self):
        self.update_conversation("That is correct!")
        self.little_boost()
        self.close_quiz()
    def on_wrong_answer(self):
        self.update_conversation("Why don't you ever listen to me")
        self.little_gaffe()
        self.close_quiz()
    def close_quiz(self):
        self.show_quiz_buttons = False
        self.show_menu_buttons = True


    def select_back(self):
        import kitchen
        kitchen.empty_scenes()
        self.done = True
    def select_talk(self):
        if len(self.remaining_trivia_keys) == 0:
            self.update_conversation("I'm tired of talking...")
        else:
            self.open_quiz()

    def select_compliment(self):
        if self.compliment_count >= 2:
            self.update_conversation("Can we do something else?")
            self.little_gaffe()
        else:
            self.update_conversation("Thank you!")
            self.little_boost()
        self.compliment_count += 1

    def select_gift(self):
        if self.gift_count >= 2:
            self.update_conversation("Can we do something else?")
            self.little_gaffe()
        else:
            items = [datingsim.player.inventory.get(key)
                for key in ('potion', 'arrows', 'tractor')]
            give = GiveDialogue(items)
            give.main_loop()
            if (give.item):
                self.update_conversation(
                    "Wow! You shouldn't have gotten me this {}".format(give.item.name))
                self.big_boost()
            else:
                self.update_conversation("What...?")
        self.gift_count += 1


    def select_photo(self):
        if self.photo_count >= 5:
            self.update_conversation("Could you just stop asking?")
            self.big_gaffe()
        elif self.photo_count >= 1:
            self.update_conversation("Didn't we already take a photo?")
            self.little_gaffe()
        else:
            self.update_conversation("Okay! Let's do that.")
            self.little_boost()
        self.photo_count += 1

    def select_kiss(self):
        if self.percentage == 100:
            if self.fail_kiss_count == 0:
                self.update_conversation("smooch")
                self.gurl.kissed = True
                # update status
        else:
            if self.fail_kiss_count == 0:
                self.update_conversation("Errr... I don't really want to.")
                self.little_gaffe()
            else:
                self.update_conversation("Errr... I don't really want to.")
                self.big_gaffe()
            self.fail_kiss_count

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

    def increase_hearts(self, increaseby):
        percentage = self.percentage + increaseby
        if percentage < 0:
            percentage = 0
        elif percentage >= 100:
            percentage = 100
        self.update_heart_meter(percentage)

    def little_boost(self):
        self.increase_hearts(3)
    def big_boost(self):
        self.increase_hearts(8)
    def little_gaffe(self):
        self.increase_hearts(-5)
    def big_gaffe(self):
        self.increase_hearts(-8)

    def main_loop(self):
        while not self.done:
            self.all_sprites.empty()
            self.buttons.empty()

            #self.all_sprites.add(self.gurl_sprite)
            self.all_sprites.add(self.back_button)
            self.buttons.add(self.back_button)

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

