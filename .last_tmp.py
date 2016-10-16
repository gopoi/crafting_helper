class Item(object):
    def __init__(self, name, *item_list):
        self.name = name
        self.item_list = item_list
    
    def __str__(self):
        return self.name
        
    def __iter__(self):
        for item in self.item_list:
            pass
    def is_basic_item(self):
        return not self.item_list
                
    def get_items(self):
        items = {}
        for item, amount in self.item_list:
            if item.name not in items:
                items[item.name] = 0
            if item.is_basic_item():
                items[item.name] += amount
            else: 
                for item_name, amount in item.get_items().items():
                    if item_name not in items:
                        items[item_name] = 0
                    items[item_name] += amount
        return items

class ItemCollection(object):
    def __init__(self, name, collection=None):
        self.name = name
        if not collection:
            self.collection == {}
        else:
            self.collection = collection

    def add_item(self, item):
        self.collection[item.name] = item
        
    def get_materials(self, item_name, multiplier=1):
        if not self.collection[item_name]:
            pass
            
charcoal=Item('charcoal')
sulfur=Item('sulfur')
gunpowder=Item('gunpowder', (sulfur,20), (charcoal, 30))
bullet = Item('bullet', (gunpowder, 10))
print(bullet.get_items())