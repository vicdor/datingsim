# Locations
def loc_the_park():
    input("Welcome to the fucking park.")
    print("""What will you do?
    (1)Play on the swings
    (2)Peer into the trash can""")

    n = range_input(2)

    if (n == 1):
        input("Yayyyyy!")
        input("Whoppeee!")
        return
    elif (n == 2):
        input("The trash can smells a little strange.")
        input("You are reminded of the city of Berkeley before "
                "you suddenly become very sleepy...")
        global location
        location = loc_dont_know
        return


def loc_your_house():
    input("You are ensconced within your middle class home.")
    input("Suddenly, a ringing from the doorbell.")
    print("""What will you do?
    (1)Exit through the back door
    (2)Check on the front door to see who's there""")

    n = range_input(2)

    if (n == 1):
        input("""Wearing your favorite diamond mocassins, you slip through
        the backdoor with grace and finesse.""")
        input("You are now at the park.")
        global location
        location = loc_the_park
        return
    elif (n == 2):
        input("You tiptoe to the door. Neglecting to peer through the "
                "peephole, you\n unwisely swing open the hinges.")
        input("FAAACK! It's Proto Krippendorf!")
        global location
        location = boy_proto_krippendorf
        return

def loc_dont_know():
    input("""You don't know where you are, but this place seems nice enough
    nevertheless. You detect a faint odor of musk.""")
    input("""Mmmmm. Smexy...""")
    print("""What will you do?
    (1) Exit the game
    (2) Return to the park""")

    n = range_input(2)

    if (n == 1):
        global location
        location = util_exit
    elif (n == 2):
        print("It seems that you cannot leave this wonderful place.")
        input("Your willpower is lacking.")
        return


#Boyz
def boy_proto_krippendorf():
    print("""You approach Proto Krippendorf. What will you do?
    (1) Discuss proto-pre-algebra
    (2) Genghis Khan
    (3) Abscond""")
    
    n = range_input(3)

    if (n == 1):
        input("Proto Krippendorf blushes.")
        input("You blush daintily.")
    elif n == 2:
        input("Proto Krippendorf glares at you")
        input("He is clearly bored, and you have clearly failed to entertain "
                "him.")
    elif n == 3:
        input("You make a mad dash for your house.")
        input("You have successfully absconded from Proto Krippendorf.")
        global location
        location = loc_your_house
        return
    else:
        input("lol wat? at boy_proto_krippendorf")

#Utility Locations
def util_exit():
    print()
    print("Thank you for playing Shitty Dating Sim.")
    quit()

#Input Utilities
def range_input(a, b=None):
    if (b == None):
        r = range(1, a+1)
    else:
        r = range(a, b)

    complete = False
    while not complete:
        try:
            n = int(input('==> '))
            if n in r:
                complete = True
            else:
                print("invalid integer")
        except ValueError:
            print("invalid input, please enter an integer")
    return n

#begin here
def main():
    global location
    location = loc_your_house

    while(location != 'quit'):
        print("current location is {}".format(location))
        location()



if (__name__ == '__main__'):
    main()
else:
    print("lol why did you import")
