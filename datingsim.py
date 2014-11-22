from dialogue import *

class Decision(object):
    """A glorified list of Choices. Represents and provides an interface to a player decision."""
    def __init__(self, choices):
        for choice in choices:
            assert isinstance(choice, Choice)
        self.choices = choices
    def add(self, choice):
        """Add another choice to this Decision."""
        assert isinstance(choice, Choice)
        self.choices.append(choice)
    def make(self, *args):
        """Carry out process for making a choice. Returns a function to call."""
        raise Error("Not yet implemented")

class RangeDecision(Decision):
    """Implements Decision by passing decision-making to command line input.
    Choices are numbered by natural numbers, and user selects choice by entering number."""
    def __init__(self, choices, decision_prompt=None):
        Decision.__init__(self, choices)
        self.decision_prompt = decision_prompt or "What will you do?"
    def make(self):
        print(self.decision_prompt)
        for i, choice in enumerate(self.choices):
            print("({num}) {desc}".format(num=i+1, desc=choice))
        n = range_input(len(self.choices)) - 1
        return self.choices[n].choose()

    @staticmethod
    def test():
        c1 = Choice("The first choice. Ao-some.", ["line1","line2","line3"],
                (lambda: print("callback c1 activated" or [1, 2, 3])))
        c2 = Choice("The sceond chocie.", [], (lambda: print ("callback 2 activated")))
        r = RangeDecision([c1, c2])
        r.make()()


class Choice(object):
    """A choice that the player can choose."""
    def __init__(self, desc, post_desc, followup, dialogue_type=SelfPacedDialogue):
        """
        @param desc: a one-line string desc of this choice
        @param post_desc: a Dialogue or a Dialogue argument that is played when this choice is chosen
        @param followup: the value that is returned when the user chooses this choice
        @param dialogue_type: the dialogue_type that is used to convert non-Dialogue post_desc
        """
        self.desc = desc
        self.followup = followup
        self.post_desc = post_desc if isinstance(post_desc, Dialogue) else dialogue_type(post_desc)
    def __str__(self):
        return self.desc
    def choose(self):
        """Called when this choice is chosen. Prints out post_desc lines and then returns followup."""
        self.post_desc.show_all()
        return self.followup

class Place(object):
    """A Place is somewhere that the player can visit, and which leads to another Place."""
    def __init__(self, visit_desc, exit, dialogue_type=SelfPacedDialogue):
        """@param visit_desc: a Dialogue or a Dialogue argument
        @param exit: either another Place, which is to be returned by self.exit(); a function,
        which is called by self.exit() to be evaluated into a Place to be returned; or a Decision
        which is made during a call to self.exit() and whose make() fn returns a Place
        @param dialogue_type: the type of Dialogue that visit_desc is converted to."""
        if isinstance(visit_desc, Dialogue):
            self.visit_desc = visit_desc
        else:
            self.visit_desc = dialogue_type(visit_desc)
        if hasattr(exit, '__call__'):  # exit is fn
            self._exit_is_fn = True
            self.exit = exit
        elif isinstance(exit, Decision):
            self._exit_is_fn = True
            self.exit = exit.make
        elif isinstance(exit, Place):
            self._exit_is_fn = False
            self._exit = exit
        else:
            raise TypeError('{} is invalid exit'.format(exit))

    def visit(self):
        """Called when player visits this place."""
        self.visit_desc.show_all()

    def exit(self):
        """Called when it's time to leave this place. Returns the next place to be visited."""
        if self._exit_is_fn:
            return self._exit()
        else:
            return self._exit

    @staticmethod
    def test():
        visit_desc = ["You are ensconced within your middle class home",
                "Suddenly, a ringing from the doorbell."]
        c1 = Choice('Exit through the back door',
                ['Wearing your favorite diamond mocassins, you slip through the backdoor with grace '
                    'and finesse.', 'You are now at the park.'], loc_the_park)
        c2 = Choice("Check on the front door to see who's there",
                ["You tiptoe to the door.",
                    "Neglecting to peer through the peephole, you unwisely swing open the hinges.",
                    "FAAAAAAAAACK! It's Proto Krippendorf!"], boy_proto_krippendorf)
        r = RangeDecision([c1, c2])
        your_house = Place(visit_desc, r)
        your_house.visit()
        print(your_house.exit())
        

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
        return loc_dont_know


def loc_dont_know():
    input("""You don't know where you are, but this place seems nice enough
    nevertheless. You detect a faint odor of musk.""")
    input("""Mmmmm. Smexy...""")
    print("""What will you do?
    (1) Exit the game
    (2) Return to the park""")

    n = range_input(2)

    if (n == 1):
        return util_exit
    elif (n == 2):
        print("It seems that you cannot leave this wonderful place.")
        input("Your willpower is lacking.")
        return


#Boyz
def boy_proto_krippendorf():
    print("""You approach Proto Krippendorf. What will you do?
    (1) Discuss proto-pre-algebra
    (2) Genghis Khan
    (3) Abscond
    (4) Beseech him to save you""")
    
    
    n = range_input(4)

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
        return loc_your_house
    elif n == 4:
        input("Krippendorf furrows his brow in concentration as he works on" \
                " granting your potentially troublesome request.")
        print("---BEGIN SAVE ATTEMPT---")

        from save import Save
        save = Save()
        data = {"location":boy_proto_krippendorf, "starting_msg": "test msg successfully loaded!"}
        save.dict["v0.1"] = data
        print("* save object generated: {}".format(str(data)))
        
        save.BURN_BABY_BURN()
        print("* save object successfully pickled.")
    else:
        input("lol wat? at boy_proto_krippendorf")

#Utility Locations
def util_exit():
    print()
    print("Thank you for playing Shitty Dating Sim.")
    quit()

#Input Utilities
def range_input(a, b=None, convert=False):
    if (b == None):
        r = range(1, a+1)
    else:
        r = range(a, b)
    return limited_input(r, int, invalid_prompt='not a choice', value_error_prompt='please enter an integer')

def limited_input(seq, process_fn=None, input_prompt=None, invalid_prompt=None, value_error_prompt=None):
    """Takes user input and processes, but only accepts that in seq"""
    process_fn = process_fn or (lambda x: x)
    prompt = input_prompt or "==> "
    invalid_prompt = invalid_prompt or 'invalid input. please try again'
    value_error_prompt = value_error_prompt or error_prompt
    complete = False
    while not complete:
        try:
            n = process_fn(input(prompt))
            if n in seq:
                complete = True
            else:
                print(invalid_prompt)
        except ValueError:
            print(value_error_prompt)
    return n
    

#begin here
def main():
    Place.test()

def load_from_save():
    # first check for existence of save
    from save import Save
    s = Save.makeFromPickle()
    if not s:
        game_loop()
    else:
        # restore existing save
        # v 0.1 save is stored as a dict in s["v0.1"]
        #    location: pointer to function of save location
        #    starting_msg: print before restoring to location
        data = s.dict["v0.1"]
        print(data["starting_msg"])
        game_loop(data["location"])
        
def game_loop(initial_loc=loc_your_house):
    prev_loc = location = initial_loc
    while(location != 'quit'):
        print("current location is {}".format(location))
        location = location()
        if location == None:
            location = prev_loc
        else:
            prev_loc = location

if (__name__ == '__main__'):
    main()
