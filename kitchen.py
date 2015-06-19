import pygame
import datingsim

def finish():
    """Requests that the game_loop stops on the next iteration. If currently in \
        world map, then stops almost immediately. If currently in some scene, \
        then stops after the current main_loop() exits."""
    datingsim.checkinit()
    global stop_request
    stop_request = True

def start():
    """Begin the game."""
    pygame.init()
    datingsim.init()
    datingsim.player.inventory.cash = 1000
    from worldmap import WorldMap
    push_scene(WorldMap())
    game_loop()

def snapshot():
    return pygame.display.get_surface().copy()

stack = []
def push_scene(scene, obliderate_stack=False):
    """
    A duck-typed scene is anything with a main_loop() method. Calling push_scene on
    the provided SCENE will add it to the stack.
    """
    global stack
    if obliderate_stack:
        stack = []
    stack.append(scene)

def pop_scene(num=1):
    global stack
    for i in range(num):
        stack.pop()

def game_loop():
    datingsim.checkinit()
    global in_game_loop, stop_request, stack
    in_game_loop = True
    stop_request = False

    try:
        while not stop_request and not len(stack) == 0:
            if len(stack) == 0:
                #TODO: how to open worldmap multiple times
                #TODO: update worldmap to add Scenes to stack rather than directly calling main_loop
                pass
            else:
                next_scene = stack[-1]
                next_scene.main_loop()
    finally:
        in_game_loop = False
