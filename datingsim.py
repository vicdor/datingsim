WIDTH, HEIGHT = RESOLUTION = 800, 600
COLOR_A = (30, 130, 200)
COLOR_B = (70, 180, 30)
COLOR_C = (120, 230, 120)  # homebrewish
COLOR_D = (0, 128, 128)  # teal
COLOR_E = (107, 142, 35)  # olive drab
COLOR_F = (160, 82, 45)  # sienna
COLOR_G = (255, 69, 0)  # orange red
import pygame
import kitchen
import locations
from player import Player
from assets import Assets


inited = False
def init():
    global inited
    if inited:
        print('warning: datingsim module already inited')
        return
    inited = True

    # unfortunately video mode has to be set in here,
    # before assets are loaded.
    global screen
    screen = pygame.display.set_mode(RESOLUTION)

    global player, assets, locs
    assets = Assets()
    player = Player()
    locs = locations.build_locs()


def quit():
    global inited, player
    inited = False
    del player

def checkinit():
    if not inited:
        raise Error("Game not yet inited!")

if __name__ == '__main__':
    kitchen.start()
