from dialogue import *
from decisions import *

class World(object):
    """A World is a dictionary-like collection of related Places. Since the same 'place' in the game
    is actually one of several different Place instances depending on the state of the World,
    (e.g. night or day), it is best that a Place store a exit as a DelayedAccesses pointing
    to a World attribute rather than a pointer to any particular Place."""
    def __init__(self, mappings=None, **kargs):
        """
        @param mappings: a dictionary that maps strings to Places
        @param **kargs: more mappings from strings to Places
        """
        if mappings:
            assert isinstance(mappings, dict)
            for key, value in mappings.items():
                assert isinstance(key, str)
                assert isinstance(value, Place)
            self._dict = mappings
        else:
            self._dict = {}

    def __get__(self, key):
        """Returns a DelayedAccess instance that delay points to the Place associated with key"""
        assert key in self._dict
        return DelayedAccess(lambda: self._dict[key])

    def __set__(self, key, value):
        """Map a string to a value, either a Place or a DelayedAccess object."""
        assert isinstance(key, str)
        assert isinstance(value, Place) or isinstance(value, DelayedAccess)
        self._dict[key] = value

class DelayedAccess(object):
    """A DelayedAccess represents a pointer that changes over time."""
    def __init__(self, pointer_fn):
        """
        @param pointer_fn: a zero-argument function is called to retrieve a pointer.
        """
        assert callable(pointer_fn)
        self.pointer_fn = pointer_fn

    def get(self):
        """Retrieves the pointer associated with this DelayedAccess instance."""
        return self.pointer_fn()


class Place(object):
    """A Place is somewhere that the player can visit, and which leads to another Place."""
    def __init__(self, name, visit_desc, exit, dialogue_type=SelfPacedDialogue):
        """
        @param name: a brief string description of this place
        @param visit_desc: a Dialogue or a Dialogue argument that is displayed when Place is visited
        @param exit: either another Place, which is to be returned by self.exit(); a function,
        which is called by self.exit() to be evaluated into a Place to be returned; or a Decision
        which is made during a call to self.exit() and whose make() fn returns a Place
        @param dialogue_type: the type of Dialogue that visit_desc is converted to."""
        assert isinstance(name, str)
        self.name = name

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
        name = "your house"
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
        your_house = Place(name, visit_desc, r)
        your_house.visit()
        print(your_house.exit())

class Waypoint(Place):
    """A Waypoint is a specialized Place with many exits."""
    def __init__(self, name, visit_desc, exits, dialogue_type=SelfPacedDialogue, exit_prompt=None, default_exit_desc=None):
        """@param exits: a list of exits, or (exits, desc_str) tuples. Exits can 
        be added later using the add_exit() fn, so it is okay to leave this empty.
        Warning: if not using tuple form, functions as exits will fail unless default_exit_desc is changed.
        @param exit_prompt: the prompt shown when the user chooses between exits. Generic default.
        @param default_exit_desc: the processing fn that is used to make exit choice descriptions 
        if exits doesn't come in (exit, desc_str) form. By default, just take the Place name attr."""
        self.exit_prompt = exit_prompt or "Where will you go?"
        self.default_exit_desc = default_exit_desc or (lambda place: place.name)

        all_tuples = True
        all_exits = True
        for e in exits:
            if isinstance(e, tuple) or isinstance(e, list):
                assert isinstance(e[1], str)
                assert isinstance(e[0], Place) or callable(e)
                all_exits = False
            else:
                assert isinstance(e, Place) or callable(e)
                all_tuples = False
        assert all_tuples ^ all_exits or len(exits) == 0

        if all_exits:
            exits = [(p, default_exit_desc(p), "You visit "+default_exit_desc(p)) for p in exits]
        choices = []
        for e, desc, post_desc in exits:
            choices.append(Choice(desc, post_desc, followup=e))
        self._decision = exit = RangeDecision(choices, self.exit_prompt)

        Place.__init__(self, name, visit_desc, exit)
            
    def add_exit(self, exit, desc, post_desc):
        assert isinstance(exit, Place) or callable(exit)
        assert isinstance(desc, str)
        self._decision.add(Choice(desc, post_desc, exit))

    @staticmethod
    def test():
        name = "your house"
        visit_desc = ["You are ensconced within your middle class home",
                "Suddenly, a ringing from the doorbell."]
        your_house = Waypoint(name, visit_desc, [])
        for _ in range(10):
            your_house.add_exit(your_house, your_house.name, [])
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

    

#begin here
def main():
    Waypoint.test()

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
