# models.py
"""
Other classes used in tree.py
"""

from dataclasses import dataclass as struct
from dataclasses import field

class Branch(object):
    Edge = "├──"
    Line = "│  "
    Corner = "└──"
    Blank = "   "
    Empty = ""

@struct
class Node:
    data: int = 0
    count: int = 1
    parent: object = None
    left: object = None
    right: object = None
    def __repr__(self):
        return str(self)
    def __str__(self):
        l = self.left.data if self.left else None
        r = self.right.data if self.right else None
        return f"Node(data={self.data}, left={l}, right={r})"
    @property
    def leaf(self):
        return not (self.left or self.right)

@struct
class DTO:
    success: bool = False
    data: list = field(default_factory=lambda: [])
    messages: list = field(default_factory=lambda: [])
    @property
    def message(self):
        return '\n'.join(self.messages)
    @classmethod
    def todo(cls):
        return cls(messages=["Not yet implemented"])

@struct
class ActionToken:
    text: str
    type: str

# TODO: ultimate objective is to get tree.py to accept input insert random 100
numeric = set('1234567890')
alpha = set('abcdefghijklmnopqrstuvwxyz')
class Interpreter(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None
        self.current_char = self.text[self.pos]

    def next_token(self):
        while self.current_char is not None:
            if self.current_char is ' ':
                while self.current_char is not None and self.current_char is ' '
                    self.pos += 1
                    if self.pos <= len(self.text) - 1:
                        self.current_char = self.text[self.pos]
                    else:
                        self.current_char = None
            if self.current_char in alpha:
                pass 

class PrefixTree:
    pass

