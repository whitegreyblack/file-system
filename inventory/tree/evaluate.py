# evaluate.py

"""
Evaluates typed tokens from interpret.py
"""

from dataclasses import dataclass as struct
from interpret import interpret, LETTER, NUMBER

@struct
class Statement:
    func: str
    args: list

from tree import Tree
print(Tree.actions)

"""
statement:
    action statement* arg*
    action arg* statement*
    action statement*
    action arg*
    action
action:
    letter
arg:
    number

Ex: insert random 100
    statement
    action statement
    action action arg
    letter letter number
    [insert, [random, 100]]

Ex: insert 1 2 3
    statement
    action arg arg arg
    [insert, 1, 2, 3]

Ex: insert 1 2 3 random 100
    statement
    action arg* statement
    action arg arg arg action arg
    [insert, 1, 2, 3, [random, 100]]

Ex: insert (random 100)
    statement
    action lparen statement rparen
    action lparen action arg rparent
    [insert, [random, 100]]

Ex: script
new
insert random 100
tree
balance
tree

new
insert 0...9 11 13
tree
balance
tree

new
insert 0...9 11 random 100 13
tree
balance
tree

new; insert 0...9; tree; balance; tree;
eval:
    t = Tree()
    for i in 0...9:
        insert i
    print(t.tree())
    t.balance()
    t.tree()

Insert syntax:
    insert 0...9
    insert random 100
    insert 0 1 2 3
"""

def evaluate(tokens):
    while tokens:
        token = tokens.pop(0)
        if token.type == LETTER:
            if token.text in Tree.actions:
                print('action: ', token.text)
            else:
                print('invalid action: ', token.text)
        else:
            print('arg: ', token.text)
    return NotImplemented

if __name__ == "__main__":
    tokens = interpret(input(">>> "))
    print(evaluate(tokens))
