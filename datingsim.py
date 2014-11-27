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
    pass
        
def game_loop(initial_place):
    prev_place = place = initial_place
    while(True):
        print("current place is {}".format(place))
        place.visit()
        place = place.exit()
        if place == None:
            place = prev_place
        else:
            prev_place = place


if (__name__ == '__main__'):
    main()
