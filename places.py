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

    def __getitem__(self, key):
        """Returns a DelayedAccess instance that delay points to the Place associated with key"""
        #assert key in self._dict
        return DelayedAccess(lambda: self._dict[key])

    def __setitem__(self, key, value):
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

    def __call__(self):
        return self.get()

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
