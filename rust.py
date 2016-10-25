from collections import defaultdict
from collections import Counter

class Item(object):
    def __init__(self, name, item_list=(), yield_amount=1):
        self.item_list = item_list
        self.name = name
        self.yield_amount = yield_amount
    
    def __str__(self):
        return self.name
 	
    def is_basic_item(self):
        return not self.item_list
                
    def get_items(self):
        items = Counter()
        items[self.name] = self.yield_amount
        for item, amount in self.item_list:
            sub_items, sub_yield_amount = item.get_items()
            items += {key: value * (amount / sub_yield_amount) for key, value in sub_items.items()}
        return items, self.yield_amount

class ItemCollection(object):
    def __init__(self, name, collection=None):
        self.name = name
        if not collection:
            self.collection = {}
        else:
            self.collection = collection

    def add_item(self, item):
        self.collection[item.name] = item
        
    def get_materials(self, item_name, multiplier=1):
        if not self.collection[item_name]:
            pass
            
charcoal=Item('charcoal')
sulfur=Item('sulfur')

cloth=Item('cloth')
metal=Item('metal fragments')
animal_fat=Item('animal fat')
low_grade_fuel=Item('low grade fuel', ((cloth, 1), (animal_fat, 3)), yield_amount=4)
gunpowder=Item('gunpowder', ((sulfur, 20), (charcoal, 30)), yield_amount=10)
explosives=Item('exlosives', ((gunpowder, 50), (low_grade_fuel, 3), (sulfur, 10), (metal, 10)))
timed_explosives=Item('timed explosives', ((explosives, 20), (cloth, 5)))

