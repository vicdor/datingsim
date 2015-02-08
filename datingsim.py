WIDTH, HEIGHT = RESOLUTION = 800, 600
import pygame
import locations
from player import Player
from assets.assets import Assets


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

def start():
    """Begin the game."""

def snapshot():
    return pygame.display.get_surface().copy()



