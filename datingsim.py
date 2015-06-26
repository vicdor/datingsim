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
    from assets import Assets
    assets = Assets()
    from player import Player
    player = Player()
    import locations
    locs = locations.build_locs()


def quit():
    global inited, player
    inited = False
    del player

def snapshot():
    return pygame.display.get_surface().copy()

def checkinit():
    if not inited:
        raise Error("Game not yet inited!")

if __name__ == '__main__':
    kitchen.start()
