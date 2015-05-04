import datingsim
from inventory import Inventory
from collections import namedtuple

class Player():

    trainable_stats = {
        'str': 'strength',
        'dex': 'dexterity',
        'spe': 'speed',
        'pow': 'power',
        'mag': 'magic',
        'cha': 'charm',
        'rom': 'romance',
        'per': 'persuasion'}

    def __init__(self):
        self.name = "Anon"
        self.day = 0
        self.str = 1
        self.dex = 1
        self.spe = 1
        self.pow = 1
        self.mag = 1
        self.cha = 1
        self.rom = 1
        self.per = 1
        self.hp = 100
        self.max_hp = 100
        item_data = [
            ('potion', 'Elven Potion', 200),
            ('sash', 'Quicksilver Sash', 300),
            ('perfume', 'Fragrant Lavendar Perfume', 400),
            ('arrows', 'Lightening Arrows', 500),
            ('tractor', 'Tractor', 600),
            ('goat', 'Billy Goat', 700)
        ]
        item_data = [(name, key, cost, 'ITEM_'+key)
                      for key, name, cost in item_data]
        self.inventory = Inventory(0, item_data)
        #Item = namedtuple('Item', ['name', 'key', 'pic', 'cost'])
        #for key, name, cost, img_key in item_data:
        #    img = datingsim.assets.get_img_safe(img_key)
        #    self.inventory[key] = [Item(name, key, img, cost), 0]

    #def get_item(self, key):
    #    return self.inventory[key][0]
    #def num_owned(self, item):
    #    return self.inventory[item.key][1]

    #def can_buy(self, item):
    #    return self.cash >= item.cost

    #def buy(self, item):
    #    if isinstance(item, str) and item in self.inventory:
    #        key = item
    #        item = self.inventory[key][0]
    #    else:
    #        key = item.key
    #    self.cash -= item.cost
    #    assert self.cash >= 0
    #    self.inventory[key][1] += 1

    @property
    def boost_multiplier(self):
        return (self.rom + self.per + 2*self.cha) / 50

    def stats_dump(self):
        """Returns str describing all stats."""
        stats = ['name', 'day', 'hp', 'cash',
                 ]
        stats += list(Player.trainable_stats.items())
        dump = ""
        for e in stats:
            if isinstance(e, str):
                #special hp/max_hp format
                if e == 'hp':
                    dump += "hp: {}/{}\n".format(self.hp, self.max_hp)
                elif e == 'cash':
                    dump += "cash: ${}\n".format(self.inventory.cash)
                else:
                    dump += "{}: {}\n".format(e, getattr(self, e))
            elif isinstance(e, tuple):
                attr, desc = e
                dump += "{}: {}\n".format(desc, getattr(self, attr))
            else:
                raise Exception("invalid stat request: {}".format(e))
        return dump
