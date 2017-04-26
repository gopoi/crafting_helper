from collections import OrderedDict
from collections import Counter
import logging
import json


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
            items += {key: value * (amount / sub_yield_amount) 
            for key, value in sub_items.items()}
        return items, self.yield_amount


class ItemCollection(object):

    def __init__(self, filename=None, name=None, collection=None):
        self.name = name
        if not collection and not filename:
            raise ValueError("collection or filename must be supplied")
        elif not collection:
            self.collection = OrderedDict()
        else:
            self.collection = collection
        if filename:
            self.import_collection_file(filename)
   
    def __iter__(self):
        yield from self.collection.items()
    
    def import_collection_file(self, filename):
        with open(filename, 'r') as file:
            item_collection = json.load(file, object_pairs_hook=OrderedDict)
        
        if {'name', 'version', 'items'} <= set(item_collection):           
            self.version = item_collection['version']
            self.name = item_collection['name']
            for item_name, item in item_collection['items'].items():
                if item_name in self.collection:
                    logging.warning("Overwriting item: {} already present in collection".format(item_name))
                if not item:
                    self.collection[item_name] = Item(item_name)
                else:
                    yield_amount = 1
                    sub_item_list = []
                    for sub_item_name, sub_yield_amount in item.items():
                        if sub_item_name == item_name:
                            yield_amount = sub_yield_amount
                        else:
                            if sub_item_name in self.collection:
                                sub_item_list.append((self.collection[sub_item_name], sub_yield_amount))
                            else:
                                raise ValueError("Trying to reference undeclared item: {}".format(sub_item_name))
                    self.collection[item_name] = Item(item_name, item_list=sub_item_list, yield_amount=yield_amount)
        else:
            raise ValueError("name, version and items must\
 be present in json item collection")

    def add_item(self, item):
        self.collection[item.name] = item
        
    def get_materials(self, item_name, multiplier=1):
        if not self.collection[item_name]:
            pass


if __name__ == '__main__':
    i = ItemCollection(filename="rust.json")
