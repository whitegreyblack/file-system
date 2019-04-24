# models/objects
from dataclasses import dataclass as struct
from dataclasses import field

@struct
class DTO:
    count: int = 0
    failure: int = 0
    success: int = 0
    early_exit: bool = False
    successful: bool = False
    databases: dict = field(default_factory=lambda: {})
    messages: list = field(default_factory=lambda: [])

    @property
    def message(self):
        return '\n'.join(self.messages)

@struct
class Item:
    name: str
    save: bool = True

ITEM, TOOL, RECIPE = range(3)

