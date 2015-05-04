import datingsim
import random

class Inventory:

    def __init__(self, starting_cash=0, item_data=None):
        """item_data should be sequence of (name, key, cost, pic_key)"""
        self.cash = starting_cash
        self.items = {}
        for args in item_data:
            self.add_new_item(*args)

    def add_new_item(self, name, key, cost, pic_key):
        self.items[key] = Item(name, key, cost, self, pic_key)
        self.items[key].quantity = 1

    def get(self, key_or_item):
        """Returns the item associated with the given key or None"""
        s = key_or_item
        if isinstance(s, Item):
            return s
        elif isinstance(s, str):
            if s in self.items:
                return self.items[s]
            else:
                raise RuntimeError(s+" is not a key corresponding to any item!")
        else:
            raise TypeError("{} is not a str!".format(s))

    def random(self):
        """Returns a random item from this inventory."""
        values = list(self.items.values())
        return random.choice(values)

    def can_buy(self, item_or_key):
        """Returns True if can purchase given item or item associated with key"""
        item = self.get(item_or_key)
        return self.cash >= item.cost

    def buy(self, item_or_key):
        """Attempts to purchase item. If cannot, throws an Error."""
        item = get(item_or_key)
        if not self.can_buy(item):
            raise RuntimeError("Cannot purchase item: {}".format(item))
        self.cash -= item.cost
        item.quantity += 1

    def can_rid(self, item_or_key):
        """Ok, now I regret making the inventory like this."""
        item = self.get(item_or_key)
        return item.quantity >= 1

    def rid(self, item_or_key):
        """Attempts to reduce item quantity by one."""
        item = self.get(item_or_key)
        if item.quantity <= 0:
            raise RuntimeError("Cannot rid item: {} {}".format(item, item.quantity))
        item.quantity -= 1

    def num_owned(self, item_or_key):
        item = self.get(item_or_key)
        return item.quantity

    def has(self, item_or_key):
        return self.num_owned(item_or_key) > 0

    def dump(self):
        """Makes a user readable info string about this inventory."""
        dump = ""
        for item in self.items.values():
            dump += "{}: {}\n".format(item.name, item.quantity)
        return dump

    def __str__(self):
        return self.dump()

class Item:
    """An instance of Item is associated with an inventory.
       It holds information about the item it represents and tracks
       the quantity of an Item owned in an Inventory.
    """
    def __init__(self, name, key, cost, inventory, pic_key=None):
        self.name = name
        self.key = key
        self.cost = cost
        self.inventory = inventory
        self.pic = datingsim.assets.get_img(key)
        self.quantity = 0

    def buy(self):
        self.inventory.buy(self)

    def can_buy(self):
        self.inventory.can_buy(self)




