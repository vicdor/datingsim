WIDTH, HEIGHT = RESOLUTION = 800, 600
COLOR_A = (30, 130, 200)
COLOR_B = (70, 180, 30)
COLOR_C = (120, 230, 120)  # homebrewish
COLOR_D = (0, 128, 128)  # teal
COLOR_E = (107, 142, 35)  # olive drab
COLOR_F = (160, 82, 45)  # sienna
COLOR_G = (255, 69, 0)  # orange red
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

def checkinit():
    if not inited:
        raise Error("Game not yet inited!")

def finish():
    """Requests that the game_loop stops on the next iteration. If currently in \
        world map, then stops almost immediately. If currently in some scene, \
        then stops after the current main_loop() exits."""
    checkinit()
    global stop_request
    stop_request = True

def start():
    """Begin the game."""

def snapshot():
    return pygame.display.get_surface().copy()

stack = []
def add_scene(scene, obliderate_stack=False):
    """
    A duck-typed scene is anything with a main_loop() method. Calling add_scene on
    the provided SCENE will add it to the stack.
    """
    global stack
    if obliderate_stack:
        stack = []
    stack.append(scene)

def game_loop():
    checkinit()
    global in_game_loop, stop_request, stack
    in_game_loop = True
    stop_request = False

    try:
        while not stop_request:
            if len(stack) == 0:
                #TODO: how to open worldmap multiple times
                #TODO: update worldmap to add Scenes to stack rather than directly calling main_loop
                pass
            else:
                next_scene = stack.pop()
                next_scene.main_loop()
    finally:
        in_game_loop = False


