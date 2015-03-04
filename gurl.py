import pygame, datingsim
import random


class Gurl:
    debug = True
    def __init__(self, name, img_dict, question_data):
        self.name = name
        self.img_dict = img_dict
        self.question_data = question_data
        self.exp = 0
        self.kissed = False;

    relationship_names = ['stranger', 'acquaintance', 'friend', 'close friend', 'gurlfriend']
    @staticmethod
    def get_relationship_num(relationship_name):
        return Gurl.relationship_names.index(relationship_name)
    @staticmethod
    def get_relationship_name(lvl):
        return Gurl.relationship_names[lvl]

    def calc_rel_level(self):
        exp = self.exp
        if exp < 1500:
            #so acquaintance can be earned with exp > 500
            exp += 1500
        level = max(exp // 2000, 0);
        if level >= len(Gurl.relationship_names) - 1:
            level = len(Gurl.relationship_names) - 1
            if not self.kissed:
                # cannot be boyfriend until kisssed
                level -= 1
        return level

    @property
    def rel_name(self):
        level = self.calc_rel_level()
        return Gurl.get_relationship_name(level)

    def do_talk(self):
        data = {}
        data[-1000] = "What the hell do you want?"
        data[0] = "And who do you think you are?"
        data[10] = "Hello."
        data[1000] = ["Here Is A Pleasant Response.", "Hello Human."]
        return self.retrieve_response(self.exp, data)

    def do_ask(self):
        data = {}
        data[-1000] = "I would like to kill you using a %weapon"
        data[0] = "Do I even know you?"
        data[100] = "My favorite color is green."
        return self.retrieve_response(self.exp, data)

    def do_give(self):
        return "do give filler"
    def do_date(self):
        return "do date filler"

    def retrieve_response(self, exp, data):
        # first find largest key <= exp
        # todo: implement %gurl_name %player_name
        def find_lt_or_eq_to(x, seq):
            best = None
            for n in seq:
                if n == x:
                    return n
                elif best == None:
                    best = n
                elif n < x and n > best:
                    best = n
            return best

        best = find_lt_or_eq_to(exp, data.keys())
        if (best == None):
            return "No response!"
        else:
            if isinstance(data[best], list):
                result = random.choice(data[best])
                return result
            else:
                return data[best]



