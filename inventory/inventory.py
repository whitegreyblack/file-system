# inventory.py
"""
Recipes will arrive in the following form

    <RecipeName> <*IngredientNames>

Any lines denotes with a '#' character are ignored. Those are comment lines.
"""
from actions import actions, add, invalid, insert
from models import *
from utils import format_words

databases = {
    'item': {},
    'recipe': {}
}

def reverse_name_index(d):
    temp = {}
    for k, v in d.items():
        temp[v.name] = k
    return temp

def insert_item(item, dictionary, from_db=False):
    for i in dictionary.items():
        print(i)
    if item not in [i.name for i in dictionary.values()]:
        index = next_index(dictionary)
        name = format_words(item)
        dictionary[index] = Item(name, from_db)
        return True
    return False

def insert_recipe(recipe, ingredients, from_db=False):
    index = next_index(databases['recipe'])
    name = format_words(recipe)
    ingredient_indexes = []
    reversed_items = reverse_name_index(databases['item'])
    for ingredient in ingredients:
        index = reversed_items.get(ingredient, None)
        if not index:
            print('Could not find ingredient in db')
            return False
        ingredient_indexes.append(index)
    databases['recipes'][index] = (recipe, ingredient_indexes, from_db)

def process_insert(inserted, value, db_name):
    if inserted:
        print(f'Inserted {value} into {db_name}')
    else:
        print(f'Insertion of {value} into {db_name} failed')

def next_index(d):
    if not d:
        return 0
    return max(d.keys()) + 1

def parse(line):
    recipe, *parts = line.split(' ')
    return recipe, parts

def build(filename, from_db):
    with open(filename, 'r') as f:
        items = [item.strip('\n') for item in f.readlines()]
    request = DTO(databases=databases)
    response = add(request, filename, *items)
    print(response.successful, response.message)
    return response

def output(dictionary):
    for k, v in dictionary.items():
        yield k, v

def output_all(databases):
    for database in databases.values():
        for k, v in output(database):
            print(k, v)

def process_recipes():
    with open('recipe') as f:
        for line in f.readlines():
            r, parts = parse(line)
            for part in parts:
                inserted = insert_item(part, 0, databases['item'])
                process_insert(inserted, part, 'item')
            inserted = insert_recipe(r, databases['recipe'], True)
            process_insert(inserted, r, 'recipe')
    
if __name__ == "__main__":
    response = build('item', from_db=True)
    output_all(response.databases)
    print(databases)
    while 1:
        try:
            user_input = input('>>> ')
        except KeyboardInterrupt:
            break
        action, *args = user_input.split(' ')
        request = DTO(databases=databases) 
        response = actions.get(action, invalid)(request, *args)
        print(response.message)
        if response.early_exit:
            break
        """ # rest of show command
            else:
                while args:
                    arg = args.pop(0)
                    if arg in 'items recipes'.split():
                        db = eval(arg)
                        if db:
                            for k, v in db.items():
                                print(k, v)
                    else:
                        print('Error parsing command. DB incorrect')
        elif action == 'make':
            while args:
                try:
                    arg_name = args.pop(0)
                except IndexError:
                    print('Unable to make item. Missing item name')
                try:
                    arg = args.pop(0)
                    arg_type = int(arg)
                except IndexError:
                    print('Unable to determine item type. Missing item type')
                except ValueError:
                    print('Unable to convert value to an item type value')
                inserted = insert_item(arg_name, arg_type, items)
                process_insert(inserted, arg_name, 'items')
        elif action == 'save':
            with open('ingredients', 'a') as f:
                for k, v in items.items():
                    if v.save and v.type == 0:
                        f.write(v.name)
            with open('tools', 'a') as f:
                for k, v in items.items():
                    if v.save and v.type == 1:
                        f.write(v.name)
        """
