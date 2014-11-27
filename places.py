from dialogue import *
from decisions import *
class World(object):
    """A World is a dictionary-like collection of Somewheres. Since the same 'place' in the game
    can be one of several different Somewhere instances depending on the state of the World,
    (e.g. night or day), it is best that a Somewhere store a exit as a DelayedAccesses pointing
    to a World attribute rather than a pointer to any particular Somewhere."""
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

    def build(self):
        """Build all Somewheres in this World."""
        for place in self._dict.values():
            place.build()

    def __getitem__(self, key):
        """Returns a DelayedAccess instance that delay points to the Somewhere associated with key."""
        return DelayedAccess(lambda: self._dict[key])

    def __setitem__(self, key, value):
        """Map a string to a Somewhere"""
        assert isinstance(key, str), key
        assert isinstance(value, Somewhere), value
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

    @staticmethod
    def soft_eval(x):
        """Accesses pointer if x is DelayedAccess, otherwise returns x unchanged"""
        if isinstance(x, DelayedAccess):
            return x.get()
        else:
            return x

    @staticmethod
    def soft_eval_list(seq):
        """Maps call_or_leave_unchanged to a sequence, returning a list."""
        [call_or_leavel_unchanged(x) for x in seq]


class Somewhere(object):
    """A somewhere has a name, can be visited, and leads to Somewhere else.
    It serves as a superclass for all Places."""
    def __init__(self, name, visit_desc, exit, dialogue_type=SelfPacedDialogue):
        """
        @param name: a string moniker for this Somewhere
        @param visit_desc: a Dialogue or list of strings that is displayed 
            when this Somewhere is visited. The list of strings in question 
            can be zero length.
        @param exit: either a Somewhere, or a zero-arg fn that returns a Somewhere.
        @param dialogue_type: the type of Dialogue that visit_desc is converted to,
            should visit_desc be a list."""
        assert isinstance(name, str)
        self.name = name

        if isinstance(visit_desc, Dialogue):
            self.visit_desc = visit_desc
        else:
            self.visit_desc = dialogue_type(visit_desc)

        if callable(exit):
            self._exit_is_fn = True
            self.exit = exit
        elif isinstance(exit, Somewhere):
            self._exit_is_fn = False
            self._exit = exit
        else:
            raise TypeError('{} is invalid exit'.format(exit))

    def build(self):
        """Call this when all exits are ready to be accessed."""
        pass

    def visit(self):
        """Called when player visits this Somewhere."""
        self.visit_desc.show_all()

    def exit(self):
        """Called when it's time to leave this Somewhere. Returns the next 
        Somewhere to be visited. Raises an Error if not yet built."""
        def check_is_somewhere(x):
            if not isinstance(x, Somewhere):
                raise TypeError("{fn} did not return a Somewhere, but returned {x}!".format(
                    fn=self._exit, x=x))
            return x

        if self._exit_is_fn:
            return check_is_somewhere(self._exit())
        else:
            return self._exit
    
    @staticmethod
    def test():
        world = World()
        world['room1'] = Somewhere('room1', ['You are entering room1'], world['room2'])
        world['room2'] = Somewhere('room2', ['You are entering room2'], world['room1'])
        world.build()
        current = world['room1'].get()
        while True:
            current.visit()
            current = current.exit()

class Place(Somewhere):
    """A Place is the standard subclass of Somewhere. A Place can have many potential exits,
    and lets the Player make the decision of choosing between these exits."""
    def __init__(self, name, visit_desc, exits=[], decision_prompt=None,
            make_choice_desc=None, **kargs):
        """
        @param name: name of this place
        @param visit_desc: this is shown when this place is visited
        @param exits: a list of valid exits. They can be added later. 
        @param exit_prompt: the prompt shown when the user chooses between exits. Generic default.
        @param make_choice_text: function that takes in a Somewhere and returns a 
            one-line description string
        """
        self.decision_prompt = decision_prompt or "Where will you go?"
        self.make_choice_desc = make_choice_desc or (lambda somewhere: somewhere.name)
        self._decision = RangeDecision([], self.decision_prompt)
        Somewhere.__init__(self, name, visit_desc, self._decision.make, **kargs)

        self._unbuilt_exits = exits
        def build():
            self._decision.empty()
            if len(self._unbuilt_exits) == 0:
                raise TypeError("Cannot build place with no exits!")
            exits = [DelayedAccess.soft_eval(exit) for exit in self._unbuilt_exits]
            for exit in exits:
                desc = self.make_choice_desc(exit)
                post_desc = []  # okay, so maybe this should be less vapid TODO
                self._decision.add(Choice(desc, post_desc, followup=exit))
        self.build = build
            
    def add_exit(self, exit):
        assert isinstance(exit, Place) or callable(exit)
        self._unbuilt_exits.append(exit)

    @staticmethod
    def test():
        world = World()
        world['room1'] = Place('room1', ['You are visiting room1', 'Rejoice.'])
        world['room2'] = room2 = Place('room2', ['You are visiting room2', 'Shudder in fear.'])
        world['room3'] = Place('room3', ['You are visiting room3'], [world['sw1'], world['room2']])
        world['sw1'] = Somewhere('sw1', ['You visit sw1', 'which leads to room3'], world['room3'])
        world['sw2'] = Somewhere('sw2', "You visit sw2", world['room1'])
        green_room = Somewhere('color room', ["You are in the Green Room",
            "You notice, as you exit this room, that it became a Red Room."], world['room1'])
        red_room = Somewhere('color room', ["You are in the Red Room",
            "You notice, as you exit this room, that it became a Green Room."], world['room1'])
        world['color room'] = green_room
        room1 = world['room1'].get()
        room1.add_exit(world['room2'])
        room1.add_exit(world['room3'])
        room1.add_exit(world['color room'])
        room2.add_exit(world['sw1'])
        world.build()

        current = room1
        while True:
            current.visit()
            if current == red_room:
                world['color room'] = green_room
                world.build()
            elif current == green_room:
                world['color room'] = red_room
                world.build()
            current = current.exit()
