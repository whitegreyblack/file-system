# actions.py

from models import *
from utils import format_words

def insert(item, database, save):
    name = format_words(item)
    if item not in database:
        database[name] = Item(name, save)
    return name in database

def add(dto, *args) -> object:
    """
    syntax:
        add [item] [args*]
        add [recipe] [arg] [args+]
    """
    args = list(args)
    db_arg = args.pop(0)
    db = dto.databases.get(db_arg, None)
    if db is None:
        dto.messages.append("""
Syntax error: Invalid database provided while parsing add command: got None""")
        return dto
    if not args:
        dto.messages.append("""
Syntax error: No arguments supplied while parsing add command""")
        return dto
    while args:
        i_arg = args.pop(0)
        inserted = insert(i_arg, db, True)
        dto.count += 1
        if inserted:
            dto.messages.append(f"Inserted {i_arg} into {db_arg}")
            dto.success += 1
        else:
            dto.messages.append(f"Could not insert {i_arg} into {db_arg}")
            dto.failure += 1
    dto.successful = dto.count == dto.success
    return dto

def show(dto, *args) -> object:
    if not dto.databases:
        dto.successful = False
    for name, db in dto.databases.items():
        dto.messages.append(f"Database: {name}")
        for k, v in db.items():
            dto.count += 1
            dto.messages.append(f"{k}: {v}")            
    dto.successful = dto.count > 0
    return dto

def leave(dto, *args) -> object:
    dto.messages.append("""
User called exit program command. Stopping application.""")
    dto.early_exit = True
    return dto

def invalid(dto, *args):
    dto.messages.append(f"Action command not found")
    dto.successful = False
    return dto

actions = {
    'exit': leave,
    'add': add,
    'insert': add,
    'ls': show,
    'show': show,
    'items': None,
    'recipes': None
}

def act(dto, action, *args) -> object:
    """
    0 -> continue
    1 -> exit
    """
    return actions.get(action, invalid)(dto, *args)
