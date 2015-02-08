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
    def remove(self, choice):
        """Remove a choice that equals given argument from this Decision.
        A ValueError is raised if the choice does not exist."""
        self.choices.remove(choice)
    def make(self, *args):
        """Carry out process for making a choice. Returns a function to call."""
        raise Error("Not yet implemented")
    def empty(self):
        """Empty this Decision of all choices."""
        self.choices = []


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
