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
    def extend(self, other):
        if not isinstance(other, DTO):
            raise TypeError("Cannot extend DTO with a non-DTO object")
        self.success = other.success
        self.messages.extend(other.messages)
    @classmethod
    def todo(cls):
        return cls(messages=["Not yet implemented"])

@struct
class ActionToken:
    text: str
    type: str

class PrefixTree:
    pass

