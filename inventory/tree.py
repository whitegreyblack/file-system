# tree.py
from dataclasses import dataclass as struct
from dataclasses import field

@struct
class Node:
    data: int = 0
    left: object = None
    right: object = None

@struct
class DTO:
    success: bool = False
    data: list = field(default_factory=lambda: [])
    messages: list = field(default_factory=lambda: [])
    @property
    def message(self):
        return '\n'.join(self.messages)

def count(root, x):
    count = 0
    nodes = [root]
    while nodes:
        node = nodes.pop(0)
        count += 1
        if node.left:
            nodes.append(node.left)
        if node.right:
            nodes.append(node.right)
    return dto(success=True, data=[count])

def delete(root, x):
    pass

def find(root, x):
    pass

def insert(root, x):
    dto = DTO()
    if not root:
        root = Node(data=x)
        dto.data.append(root)
        dto.success = True
        dto.messages.append(f"Root was empty. Inserting {x} as root")
        return dto
    node = Node(data=x)
    temp = root
    if temp:
        dto.messages.append(f"Root was not empty. Starting descent with root.")
        dto.messages.append(f"Current node being viewed is {temp.data}")
    while temp:
        smaller = x <= temp.data
        if smaller:
            dto.messages.append(f"{x} is smaller or equal to temp data. Going left.")
            temp = temp.left
        else:
            dto.messages.append(f"{x} is larger than temp data. Going right.")
            temp = temp.right
    temp = node
    print(root, root.left, root.right)
    dto.messages.append(f"Inserting {x}")
    dto.data.append(root)
    return dto

def tree(x):
    print(x, x.left, x.right)

def parse(dto):
    response = DTO()
    for d in dto.data:
        try:
            response.data.append(int(d.strip()))
        except ValueError:
            response.messages.append("Error converting {d} to int")
    response.success = bool(len(response.data))
    if not response.success:
        response.messages.append("No valid arguments parsed")
    return response

if __name__ == "__main__":
    actions = {
        'insert': insert,
        'delete': delete,
        'count': count,
        'find': find,
        'tree': tree
    }
    ROOT = Node(data=5)
    while 1:
        action, *args = input('>>> ').split(' ')
        if action == 'exit':
            break
        if action not in actions:
            print("Command not found")
            continue
        request = DTO(data=args)
        response = parse(request)
        if response.message:
            print(response.message)
        if not response.success:
            continue
        for x in response.data:
            response = actions[action](ROOT, x)
            tree(ROOT)
            print(response.message)

