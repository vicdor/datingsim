import pygame, datingsim
from shop import GiveDialogue
import random


class Gurl:
    debug = True
    def __init__(self, name, img_dict, talk_data, ask_data=None, quiz_data=None,
                 ):
        self.name = name
        self.img_dict = img_dict
        self.talk_data = talk_data
        self.ask_data = ask_data or Gurl.default_ask_data
        self.quiz_data = quiz_data or Gurl.default_quiz_data
        self.trivia = {}
        self.spoofs = {}
        self.quiz_questions = {}
        self.exp = 0
        self.kissed = False
        self.gaff_count = 0

    def set_trivia(self, key, answer, spoofs, quiz_question):
        """Remember to call this after initializing ur Gurl."""
        self.trivia[key] = answer
        self.spoofs[key] = spoofs
        self.quiz_questions[key] = quiz_question

    def default_img(self):
        return self.img_dict['default']


    default_ask_data = {}
    default_quiz_data = {}
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
        return int(level)

    @property
    def rel_name(self):
        level = self.calc_rel_level()
        return Gurl.get_relationship_name(level)

    def do_talk(self, data=None):
        data = data or self.talk_data
        self.mini_boost()
        return self.retrieve_response(self.exp, data)

    def do_ask(self, data=None):
        data = data or self.ask_data
        self.mini_boost()
        return self.retrieve_response(self.exp, data).format(**self.trivia)

    def do_give(self):
        items = [datingsim.player.inventory.get(key)
                 for key in ('potion', 'arrows', 'tractor')]
        give = GiveDialogue(items)
        give.main_loop()
        if (give.item):
            return "Thank you! I love this {}.".format(give.item.name)
        else:
            return "What? I thought you were going to give me a present."

    def do_date(self):
        return "do date filler"

    def _boost_helper(self, base_boost):
        self.exp += min(1, base_boost * datingsim.player.boost_multiplier)

    def mini_boost(self):
        """boost from talking or giving a mediocre item"""
        self._boost_helper(5)

    def micro_boost(self):
        """boost from phone chat, or for friendly gurls, just meeting"""
        self._boost_helper(1)

    def boost(self):
        """another boost size... probably for entering a date"""
        self._boost_helper(15)

    def mega_boost(self):
        """not sure what this is going to be used for"""
        self._boost_helper(50)

    def gaff(self):
        """do something stupid"""
        self.exp -= 20
        self.gaff_count += 1

    def mega_gaff(self):
        """do something really stupid"""
        self.exp -= 100
        self.gaff_count += 7

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

class Kanaya(Gurl):
    def __init__(self):
        gurl_imgs = {}
        gurl_imgs['askance'] = datingsim.assets.get_img_safe('GURL_kanaya_askance')
        gurl_imgs['happy'] = gurl_imgs['default'] = datingsim.assets.get_img_safe('GURL_kanaya_smile')

        talk_data = {}
        talk_data[-1000] = "What the hell do you want?"
        talk_data[0] = "And who do you think you are?"
        talk_data[10] = "Hello."
        talk_data[100] = ["How are you?", "How do you do?", "What's up?", "Nice seeing you again."]
        talk_data[1000] = ["How are you?", "Nice seeing you again. (He's worth it!)"]

        ask_data = {}
        ask_data[0] = "Nice to meet you. I am Kanaya."
        ask_data[100] = ["I am {height} cm tall.", "I am {age} years of age.",
                         "My waist circumference is {waist} cm.",
                         "My phone number is {phone}."]
        quiz_data = {}
        Gurl.__init__(self, "Kanaya", gurl_imgs, talk_data, ask_data, quiz_data)
        self.set_trivia("height", 120, [121, 123, 124], "What is my height?")
        self.set_trivia("age", 14, [12, 13, 15], "How old am I?")
        self.set_trivia("waist", 40, [37, 50, 9001], "What are my waist measurements?")
        self.set_trivia("phone", "236-1673", ["125-7234", "922-0117", "237-9115"],
                        "What is my phone number?")

class Isadora(Gurl):
    def __init__(self):
        gurl_imgs = {}
        gurl_imgs['default'] = datingsim.assets.get_img_safe('GURL_isadora_default');

        talk_data = {}
        talk_data[-1000] = "What the hell do you want?"
        talk_data[0] = "And who do you think you are?"
        talk_data[10] = "Hello."
        talk_data[100] = ["How are you?", "How do you do?", "What's up?", "Nice seeing you again."]
        talk_data[1000] = ["How are you?", "Nice seeing you again. (He's worth it!)"]

        ask_data = {}
        ask_data[0] = "Nice to meet you. I am Isadora."
        ask_data[100] = ["I am {height} cm tall.", "I am {age} years of age.",
                         "My waist circumference is {waist} cm.",
                         "My phone number is {phone}."]
        quiz_data = {}
        Gurl.__init__(self, "Kanaya", gurl_imgs, talk_data, ask_data, quiz_data)
        self.set_trivia("height", 120, [121, 123, 124], "What is my height?")
        self.set_trivia("age", 14, [12, 13, 15], "How old am I?")
        self.set_trivia("waist", 40, [37, 50, 9001], "What are my waist measurements?")
        self.set_trivia("phone", "236-1673", ["125-7234", "922-0117", "237-9115"],
                        "What is my phone number?")



