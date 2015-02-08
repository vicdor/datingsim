import pygame, pygame.display, pygame.mixer
from pygame.locals import *
import datingsim
from button import *
from dreambutton import *
from dialogue import CoolDialogue

pygame.init()
GAME_WIDTH, GAME_HEIGHT = 800, 400
pygame.display.set_caption('display test')
screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))

def title_state():
    font = pygame.font.Font(None, 80)
    text = 'Dating Sim 3000'

    fg = 0, 0, 0
    bg = 10, 140, 40
    size = font.size(text)
    ren = font.render(text, 0, fg, bg)
    screen.blit(ren, [10, 10])

    text = "Press SPACE to continue"
    alpha_iter = list(range(255, 0,-1))+list(range(0, 255))
    alpha_index = 0
    width, height = font.size(text)
    rend = font.render(text, False, [255, 255, 255])
    screen.blit(rend, [100, GAME_WIDTH/2-width/2])

    def draw_instruct():
        nonlocal alpha_index
        alpha_index = (alpha_index + 3) % len(alpha_iter)
        rend.set_alpha(alpha_iter[alpha_index])
        screen.blit(rend, [200, GAME_WIDTH/2-width/2])

    pygame.display.flip()

    pygame.mixer.music.load('forest.wav')
    pygame.mixer.music.play()

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type in (QUIT, KEYDOWN, KEYUP):
                done = True

        screen.fill(bg)
        screen.blit(ren, [10, 10])
        draw_instruct()
        pygame.display.flip()
        pygame.time.wait(1000//20)

    pygame.mixer.music.stop()

class AttributeSlider(pygame.sprite.Sprite):
    points_available = 3
    min_points = 5
    prev_y = None
    def __init__(self, attr_name, starting_val=10):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.attr_name = attr_name
        self.attr_value = starting_val
        self.font = pygame.font.Font(None, 50)
        self.update()

        if not AttributeSlider.prev_y:
            AttributeSlider.prev_y = 100
            self.make_points_disp()
        else:
            AttributeSlider.prev_y += 30
        rectx = 10
        recty = AttributeSlider.prev_y
        self.rect = self.image.get_rect().move(rectx, recty)
        sizex, sizey = self.font.size(self.text)
        spacing = 10
        button_size = sizey * .7

        def add():
            if AttributeSlider.points_available > 0:
                self.attr_value += 1
                AttributeSlider.points_available -= 1
        def sub():
            if self.attr_value > AttributeSlider.min_points:
                self.attr_value -= 1
                AttributeSlider.points_available += 1

        rectx, recty = self.rect.x, self.rect.y
        add_button = BlockButton(add, pygame.Color('blue'), pos=(rectx+sizex+spacing, recty),
                                 text='+')
        sub_button = BlockButton(sub, pygame.Color('red'),
                pos=(rectx+sizex+button_size + 2*spacing, recty), text='-')

    def update(self):
        self.text = "{}: {}".format(self.attr_name, self.attr_value)
        sizex, sizey = self.font.size(self.text)
        spacing = 10
        button_size = sizey * .7
        surf = pygame.Surface([sizex, sizey], flags=pygame.SRCALPHA)
        text_rend = self.font.render(self.text, False, [50, 0, 100])
        surf.blit(text_rend, [0, 0])
        self.image = surf

    def make_points_disp(self):
        """lack of a better name. Makes the display that shows how many points left"""
        PointsDisp([10, 60], pygame.font.Font(None, 20), (200, 30, 150))

def center_text(text, font, font_color, rect, surf):
    """blits the text into the center of rect on surf"""
    t_surf = font.render(text, False, font_color)
    W, H = rect.size
    w, h = t_surf.get_size()
    x = (W - w) / 2
    y = (H - h) / 2
    surf.blit(t_surf, [x, y])

class PointsDisp(pygame.sprite.Sprite):
    """For make_points_disp"""
    def __init__(self, pos, font, font_color):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.font = font
        self.font_color = font_color
        self.update()
        self.rect = self.image.get_rect().move(pos)

    def update(self):
        text = "points remaining: {}".format(AttributeSlider.points_available)
        surf = pygame.Surface([GAME_WIDTH, 40])
        center_text(text, self.font, self.font_color, surf.get_rect(), surf)
        self.image = surf

def stat_select():
    bg_color = pygame.Color('black')
    all_sprites = pygame.sprite.Group()
    attributes = pygame.sprite.Group()
    buttons = pygame.sprite.Group()

    AttributeSlider.containers = [all_sprites, attributes]
    Button.containers = [all_sprites, buttons]
    PointsDisp.containers = all_sprites

    font = pygame.font.Font(None, 40)
    font.set_underline(True)
    title_surf = font.render('Build Character Stats', False, pygame.Color('white'))
    title_x = (GAME_WIDTH - title_surf.get_width()) / 2
    title_y = 10
    def blit_title():
        screen.blit(title_surf, [title_x, title_y])

    strength = AttributeSlider("strength")
    dexterity = AttributeSlider("dextricity")
    speed = AttributeSlider("speed")
    sliders = [AttributeSlider(attr) for attr in
               'strength dexterity speed luck magic romance persuasion'.split()]

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type is QUIT:
                quit()
            if event.type is pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.rect.collidepoint(event.pos):
                        button.on_click()
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_RETURN]:
            done = True
        all_sprites.update()
        screen.fill(bg_color)
        all_sprites.draw(screen)
        blit_title()
        pygame.display.flip()

        pygame.time.wait(1000//12)

    global stats
    stats = {a.attr_name: a.attr_value for a in sliders}


# title_state()
# stat_select()
# while location != 'omg quit already':
#     location()
