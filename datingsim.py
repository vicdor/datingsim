from dialogue import *
from decisions import *
from places import *


def loc_your_house():
    input("You are ensconced within your middle class home.")
    input("Suddenly, a ringing from the doorbell.")
    c1 = Choice('Exit through the back door',
            ['Wearing your favorite diamond mocassins, you slip through the backdoor with grace '
                'and finesse.', 'You are now at the park.'], loc_the_park)
    c2 = Choice("Check on the front door to see who's there",
            ["You tiptoe to the door.",
                "Neglecting to peer through the peephole, you unwisely swing open the hinges.",
                "FAAAAAAAAACK! It's Proto Krippendorf!"], boy_proto_krippendorf)
    r = RangeDecision([c1, c2])
    r.add(c2)
    return r.make()


#Utility Locations
def util_exit():
    print()
    print("Thank you for playing Shitty Dating Sim.")
    quit()
#begin here
def main():
    game_loop(world['br'].get())
        
def game_loop(initial_place):
    prev_place = place = initial_place
    while(True):
        place.visit()
        place = place.exit()
        if place == None:
            place = prev_place
        else:
            prev_place = place

world = World()
world['br_window'] = Somewhere('bedroom window', ['What a gorgeous day it is outside.',
    'Unfortunately, even from inside your bedroom you can here the rancorous cry of scrub jay.',
    'What an awful noise. You back off back into the middle of your room.'], world['br'])
world['wardrobe'] = Somewhere('wardrobe', ['Nothing interesting in here.',
    'So you turn back around.'], world['br'])
world['br'] = Place('your bedroom', ['You stand in the middle of your bedroom',
    "You can't help but take another glance at the calculus and physics equations on the ceiling.",
    'Hmmm... What to do, what to do?'], [world['br_window'], world['wardrobe'], world['hallway']])
world['hallway'] = Place('hallway', ['You are in your upstairs hallway.',
    'To your left is your bedroom, and on the right is the study.',
    'Of course, you could aways go back downstairs and check out the living room.',
    'So... what will you do?'], [world['br'], world['study'], world['living_room']])
world['study'] = Somewhere('study', ['Ehh... looks like Dad is in here.',
    'You back off before disturbing his Supreme Concentration.'], world['hallway'])
world['living_room'] = Place('living room',
    ['You enter the living room, which appears cluttered as usual.', 'Your Macbook Air is placed'
        + " precariously on the arm of the sofa,",
        "but you don't feel like dealing with that right now.",
        "Guess it's time to go somewhere else."], [world['piano_room'], world['hallway']])
world['piano_room'] = Somewhere('piano room', ["Before leaving the piano room, you first"
    + " play a mysteriously familiar Haunting Refrain."], world['living_room'])
world.build()


if (__name__ == '__main__'):
    main()
