import datingsim
from inventory import Inventory
from collections import namedtuple

class Player():
    name = "Anon"
    day = 0
    str = 1
    dex = 1
    spe = 1
    pow = 1
    mag = 1
    cha = 1
    rom = 1
    per = 1
    #cash = 0
    hp = 100
    max_hp = 100

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
                else:
                    dump += "{}: {}\n".format(e, getattr(self, e))
            elif isinstance(e, tuple):
                attr, desc = e
                dump += "{}: {}\n".format(desc, getattr(self, attr))
            else:
                raise Exception("invalid stat request: {}".format(e))
        return dump

    #def inventory_dump(self):
    #    dump = ""
    #    for item, count in self.inventory.values():
    #        dump += "{}: {}\n".format(item.name, count)
    #    return dump

