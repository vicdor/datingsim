import pygame
import datingsim
import random
from dialogue import CoolDialogue
from shop import CoolShop
from datingsim import WIDTH, HEIGHT, RESOLUTION
from button import BlockButton

class LocButton(BlockButton):
    i = 0
    b_start_pos = [20, 20]
    b_w, b_h = 80, 50
    b_spacing = 10
    def __init__(self, on_click, text, color=(100, 130, 180), **style):
        L = LocButton
        x = L.b_start_pos[0]
        y = L.b_start_pos[1] + L.i*(L.b_h + L.b_spacing)
        pos = (x, y)
        size = (L.b_w, L.b_h)
        BlockButton.__init__(self, on_click, color, size, pos, text, **style)
        L.i += 1
    @staticmethod
    def reset():
        """resets class variables so buttons for a new Location can be made"""
        LocButton.i = 0
        LocButton.containers = None

class LocButton2(BlockButton):
    """LocButtons that appear on the right side of the screen"""
    j = 0
    m_spacing = LocButton.b_spacing
    m_start_pos_r = [WIDTH - 160, 20]
    b2_w, b2_h = 130, 50

    def __init__(self, on_click, text, color=(30, 130, 180), **style):
        L2 = LocButton2
        x = L2.m_start_pos_r[0]
        y = L2.m_start_pos_r[1] + L2.j*(L2.b2_h + L2.m_spacing)
        pos = (x, y)
        size = (L2.b2_w, L2.b2_h)
        BlockButton.__init__(self, on_click, color, size, pos, text, **style)
        L2.j += 1

    @staticmethod
    def reset():
        LocButton2.j = 0
        LocButton2.containers = None

class BackToMap(BlockButton):
    pos = (WIDTH - 160, HEIGHT - 70)
    w, h = size = (130, 50)

    def __init__(self, on_click=None, color=(50, 20, 120), **style):
        assert hasattr(BackToMap, 'containers'), 'no containers... DERRRRRRRR HUURRRRRRR'
        B = BackToMap
        def go_back():
            CoolDialogue('Go back to world map filler.').main_loop()
        BlockButton.__init__(self, on_click or go_back, color, B.size, B.pos,
                                "Go back!", **style)

class QuickSleepButton(BlockButton):
    pos = (20, HEIGHT - 70)
    w, h = size = (80, 80)

    def __init__(self, color=(40, 120, 20), **style):
        Q = QuickSleepButton
        def do_nap():
            p = datingsim.player
            p.hp = p.max_hp
            p.day += 1
            text = ("HP restored!\n"
                    "It is now day {}.").format(p.day)
            CoolDialogue(text).main_loop()
        BlockButton.__init__(self, do_nap, color, Q.size, Q.pos, "Quick Sleep")

class CashHPText(pygame.sprite.Sprite):

    def __init__(self, pos, font=None, font_color=(123, 67, 98)):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.font = font or pygame.font.Font(None, 20)
        self.font_color = font_color
        self.update()
        self.rect = self.image.get_rect().move(pos)

    def update(self):
        p = datingsim.player
        text = "$:{}      HP:{}".format(p.inventory.cash, p.hp)
        self.image = self.font.render(text, False, self.font_color)

class Location():
    WASH_COLOR = (0, 0, 0)
    _dict = None

    def __init__(self, button_data, name=None, bg_img=None):
        """button_data is taken as a list of 2-tuples with button name and
        button on_click fns."""
        self.button_data = button_data
        self.bg_img = bg_img
        self.name = name

    def enter(self):
        """The player enters this location in the dating sim"""
        all_sprites = pygame.sprite.Group()
        buttons = pygame.sprite.Group()


        # generate Location-specific buttons
        LocButton.reset()
        LocButton.containers = [all_sprites, buttons]
        for name, on_click in self.button_data:
            LocButton(on_click, name)

        # generate generic menu buttons
        LocButton2.reset()
        LocButton2.containers = [all_sprites, buttons]
        dumby_fn = lambda: None
        def inventory_fn():
            text = datingsim.player.inventory_dump()
            d = CoolDialogue(text, snapshot=datingsim.snapshot())
            d.main_loop()
        def statistics_fn():
            text = datingsim.player.stats_dump()
            CoolDialogue(text, snapshot=datingsim.snapshot()).main_loop()
        LocButton2(dumby_fn, 'Location Name')
        LocButton2(inventory_fn, 'Inventory')
        LocButton2(statistics_fn, 'Statistics')

        BackToMap.containers = [all_sprites, buttons]
        def on_click_back():
            nonlocal done
            done = True
        BackToMap(on_click_back)

        QuickSleepButton.containers = [all_sprites, buttons]
        QuickSleepButton()


        # cash and HP display text
        cash_text_loc = (200, HEIGHT-30)
        CashHPText.containers = [all_sprites]
        CashHPText(cash_text_loc)

        # okay, and now we loop
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type is pygame.QUIT:
                    done = True
                elif event.type is pygame.MOUSEBUTTONDOWN:
                    for button in buttons:
                        if button.rect.collidepoint(event.pos):
                            # TODO: consider whether this is worth implementing
                            # if location switches, button is expected to change
                            # global variable location and return True
                            # done = button.on_click() or False
                            button.on_click()
                all_sprites.update()
                datingsim.screen.fill(self.WASH_COLOR)
                if self.bg_img:
                    datingsim.screen.blit(self.bg_img, [0,0])
                all_sprites.draw(datingsim.screen)
                # blit_title()
                # update_text()
                # screen.blit(text_surf, text_loc)
                pygame.display.flip()
                pygame.time.wait(1000//20)

    @staticmethod
    def test():
        pygame.init()
        datingsim.init()

        def do_jog():
            p = datingsim.player
            cost = 30
            if p.hp < cost:
                text = "Not enough hp."
            else:
                p.hp -= cost
                spe_ch = random.randint(1, 5)
                dex_ch = random.randint(1, 3)
                p.spe += spe_ch
                p.dex += dex_ch
                text = ("Speed increased by {}.\n"
                        "Dexterity increased by {}.\n"
                        ).format(spe_ch, dex_ch)
            CoolDialogue(text).main_loop()
        button_data = [('wowz', lambda: print('hai')),
                    ('lolz', lambda: print("lol")),
                    ('Jog', do_jog)]
        bg_img = datingsim.assets['NZ_map']
        loc = Location(button_data, bg_img)
        loc.enter()

        datingsim.quit()
        pygame.quit()

    @staticmethod
    def test2():
        pygame.init()
        datingsim.init()
        #loc = random.choice(list(datingsim.locs.values()))
        loc = datingsim.locs['castle']
        loc.enter()
        datingsim.quit()
        pygame.quit()

    @staticmethod
    def test3():
        pygame.init()
        datingsim.init()

        done = False
        def end_program():
            nonlocal done
            done = True
            print("\nGood day to you, you handsome bastard, you.")

        while not done:
            try:
                loc_key = input("Where do you want to visit?")
                datingsim.locs[loc_key].enter()
            except KeyboardInterrupt:
                end_program()
            except EOFError:
                end_program()
            except KeyError:
                print("location not defined.")

        datingsim.quit()
        pygame.quit()


def build_locs():
    """Returns a dictionary of preset locs for this game."""
    #begin utility fns for button actions
    hp_text = "Not enough HP!"
    def try_expend_hp(amount, auto_admonish=True):
        """Attempts to expend hp. Returns bool flag indicating success."""
        p = datingsim.player
        if p.hp < amount:
            if auto_admonish:
                show_dialogue(hp_text)
            return False
        else:
            p.hp -= amount
            return True

    cash_text = "Not enough $$$!"
    def try_expend_cash(amount, auto_admonish=True):
        p = datingsim.player
        if p.cash < amount:
            if auto_admonish:
                show_dialogue(cash_text)
            return False
        else:
            p.cash -= amount
            return True

    def show_dialogue(text, **style):
        snapshot = pygame.display.get_surface().copy()
        CoolDialogue(text, snapshot=snapshot, **style).main_loop()

    def filler():
        show_dialogue('filler')

    def show_shop(item_keys, **style):
        snapshot = pygame.display.get_surface().copy()
        p = datingsim.player
        s = CoolShop([p.inventory.get(key) for key in item_keys])
        s.main_loop()

    def make_work_fn(hp_cost, profit_fn):
        """profit_fn takes in an argument p, a reference to player."""
        def awesome_job_awesome():
            p = datingsim.player
            if not try_expend_hp(hp_cost):
                return
            cash_inc = round(profit_fn(datingsim.player)) or 1
            p.inventory.cash += cash_inc
            text = ("You earned ${}."
                    ).format(cash_inc)
            show_dialogue(text)
        return awesome_job_awesome

    #begin creating templates for buttons
    def do_sleep():
        p = datingsim.player
        p.hp = p.max_hp
        p.day += 1
        show_dialogue("HP Restored! \nIt is now day {}.".format(p.day))
    sleep_data = ('Sleep', do_sleep, 'restore HP')

    def do_save_game():
        text = ("Here is a filler for saving your game!"
                "How incredibly delightful!")
        show_dialogue(text)
    save_game_data = ('Save Game', do_save_game, 'save game data')

    def do_phone():
        text = ("Here is the filler for phoning a farm animal.")
        show_dialogue(text)
    phone_data = ('Phone', do_phone, 'phone a girl -5 hp')

    def do_swim():
        p = datingsim.player
        if not try_expend_hp(40):
            return
        spd_inc, str_inc = random.randint(2,5), random.randint(2,5)
        p.spe += spd_inc
        p.str += str_inc
        text = ("Speed increased by {}.\n"
                "Strength increased by {}.\n"
                ).format(spd_inc, str_inc)
        show_dialogue(text)
    swim_data = ('Swim', do_swim, 'train SPD + STR')

    def do_sun_bathe():
        p = datingsim.player
        if not try_expend_hp(30):
            return
        per_inc = random.randint(2,5)
        p.per += per_inc
        text = ("Persuasion increased by {}."
                ).format(per_inc)
        show_dialogue(text)
    sun_bathe_data = ('Sun Bathe', do_sun_bathe, 'train persuasion')

    def do_club_date():
        text = ("Here is the filler for dating.")
        show_dialogue(text)
    club_date_data = ('Date', do_club_date, 'meet some girls')

    def do_drink():
        if not try_expend_hp(20) or not try_expend_cash(20):
            return
        charm_inc = randint(3,7)
        text = ("Buuuuurp.\n"
                "Charm increased by {}.\n"
                ).format(charm_inc)
        show_dialogue(text)
    drink_data = ('Drink', do_drink, '20 gold, 20 HP\nraise charm')

    do_mountain_shop = lambda: show_shop(['potion', 'sash', 'perfume'])
    mountain_shop_data = ('Shop', do_mountain_shop, 'buy some items')
    do_castle_shop = lambda: show_shop(['arrows', 'tractor', 'goat'])
    castle_shop_data = ('Shop', do_castle_shop, 'buy some items')

    def do_romance():
        p = datingsim.player
        if not try_expend_hp(20):
            return
        rom_inc = random.randint(1,3)
        p.rom += rom_inc
        text = ("Romance increased by {}!"
                ).format(rom_inc)
    romance_data = ('Romance', do_romance, 'cost 20 hp')

    relax_data = ('Relax', filler, 'lay low for a while')
    river_date_data = ('Date', filler, 'meet some girls')
    #casino skipped
    do_dark_city_work = make_work_fn(50, lambda p: p.str * 1.5)
    dark_city_work_data = ('Work', do_dark_city_work, 'wage = strength x 1.5')

    do_woods_work = make_work_fn(50, lambda p: p.spe * 1.5)
    woods_work_data = ('Work', do_woods_work, 'wage = speed x 1.5')

    do_inn_work = make_work_fn(50, lambda p: p.per * 1.75)
    inn_work_data = ('Work', do_inn_work, 'wage = persuasion x 1.75')

    do_castle_work = make_work_fn(50, lambda p: p.mag * 1.5)
    castle_work_data = ('Work', do_castle_work, 'wage = magic*1.50')

    do_gym_work = make_work_fn(50, lambda p: p.per + p.cha)
    gym_work_data = ('Work', do_gym_work, 'wage=persuasion+charm')

    do_clinic_work = make_work_fn(50, lambda p: p.cha + p.per)
    clinic_work_data = ('Work', do_clinic_work, 'Work (wage = charm + persuasion')

    do_plunder = make_work_fn(100,
        lambda p: p.pow + p.spe*random.uniform(0.1,5.0))
    plunder_data = ('Plunder', do_plunder, 'random profit')

    glinda_visit_data = ('Glinda', filler, 'pay a visit')
    elphaba_visit_data = ('Elphaba', filler, 'pay a visit')
    nessarose_visit_data = ('Nessarose', filler, 'pay a visit')
    eponine_visit_data = ('Eponine', filler, 'pay a visit')
    fantine_visit_data = ('Fantine', filler, 'pay a visit')
    cosette_visit_data = ('Cosette', filler, 'pay a visit')

    def do_train_magic():
        p = datingsim.player
        if not try_expend_hp(20):
            return
        magic_inc = random.randint(2,4)
        p.mag += magic_inc
        text = ("Magic increased by {}!"
                ).format(magic_inc)
        show_dialogue(text)
    train_magic_data = ('Train Magic', do_train_magic, 'cost 20 hp')

    def do_train_speed():
        p = datingsim.player
        if not try_expend_hp(20):
            return
        spe_inc = random.randint(2, 4)
        p.spe += spe_inc
        text = ("Speed increased by {}!"
                ).format(spe_inc)
        show_dialogue(text)
    train_speed_data = ('Train Speed', do_train_speed, 'cost 20 hp')

    def do_train_power():
        p = datingsim.player
        if not try_expend_hp(20):
            return
        pow_inc = random.randint(2, 4)
        p.pow += pow_inc
        text = ("Power increased by {}!"
                ).format(pow_inc)
        show_dialogue(text)
    train_power_data = ('Train Power', do_train_power, 'cost 20 hp')

    def do_workout():
        p = datingsim.player
        if not try_expend_hp(100):
            return
        text = ''
        for stat, stat_name in p.trainable_stats.items():
            increase = random.randint(0,3)
            if increase > 0:
                orig_val = getattr(p, stat)
                setattr(p, stat, orig_val + increase)
                stat_name = stat_name.capitalize()
                line = "{} increased by {}!\n".format(stat_name, increase)
                text += line
        show_dialogue(text)
    workout_data = ('Workout', do_workout, '100 hp, train all stats')

    # begin adding locations to dict
    _dict = {}
    def add_loc(name, button_data, key=None, bg_img=None, **style):
        key = key or name.lower()
        # temporary TODO: allow for desc text
        button_data = [tup[:2] for tup in button_data]
        _dict[key] = Location(button_data, bg_img=bg_img, name=name, **style)

    add_loc("Home", [sleep_data, save_game_data, phone_data],
            bg_img=datingsim.assets.get_img_safe('BG_home'))
    add_loc("Beach of the East", [swim_data, sun_bathe_data],
            key='beach_east',
            bg_img=datingsim.assets.get_img_safe('BG_beach_east'))
    add_loc("Beach of the West", [swim_data, sun_bathe_data],
            key='beach_west',
            bg_img=datingsim.assets.get_img_safe('BG_beach_west'))
    add_loc("Night Club", [club_date_data, drink_data],
            bg_img=datingsim.assets.get_img_safe('BG_club'),
            key='club')
    add_loc("Clinic", [clinic_work_data],
            bg_img=datingsim.assets.get_img_safe('BG_clinic'),
            key='clinic')
    add_loc("Mountain", [mountain_shop_data],
            bg_img=datingsim.assets.get_img_safe('BG_mountain'),
            key='mountain')
    add_loc("Hot Springs", [romance_data, relax_data],
            bg_img=datingsim.assets.get_img_safe('BG_springs'),
            key='springs')
    add_loc("Great River", [river_date_data],
            bg_img=datingsim.assets.get_img_safe('BG_river'),
            key='river')
    add_loc("Casino", [],
            bg_img=datingsim.assets.get_img_safe('BG_casino'),
            key='casino')
    add_loc("Dark City", [dark_city_work_data],
            bg_img=datingsim.assets.get_img_safe('BG_dark_city'),
            key='city')
    add_loc("The Woods", [woods_work_data, relax_data],
            bg_img=datingsim.assets.get_img_safe('BG_woods'),
            key='woods')
    add_loc("The Village",
            [glinda_visit_data, elphaba_visit_data, nessarose_visit_data,
             eponine_visit_data, fantine_visit_data, cosette_visit_data],
            bg_img=datingsim.assets.get_img_safe('BG_village'),
            key='village')
    add_loc("Town Inn",
            [inn_work_data, plunder_data],
            bg_img=datingsim.assets.get_img_safe('BG_inn'),
            key='inn')
    add_loc("Royal Castle",
            [castle_work_data, plunder_data, castle_shop_data],
            bg_img=datingsim.assets.get_img_safe('BG_castle'),
            key='castle')
    add_loc("Twilight Valley",
            [train_magic_data, train_power_data, train_speed_data],
            bg_img=datingsim.assets.get_img_safe('BG_valley'),
            key='valley')
    add_loc("Training Area",
            [gym_work_data, workout_data],
            bg_img=datingsim.assets.get_img_safe('BG_gym'),
            key='gym')
    add_loc("Arcade",
            [],
            key='arcade')
    return _dict


if __name__ == '__main__':
    Location.test2()
