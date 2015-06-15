WIDTH, HEIGHT = RESOLUTION = 800, 600
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
