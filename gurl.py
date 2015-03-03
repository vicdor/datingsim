import pygame, datingsim


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
        return "do talk filler"
    def do_ask(self):
        return "do ask filler"
    def do_give(self):
        return "do give filler"
    def do_date(self):
        return "do date filler"





