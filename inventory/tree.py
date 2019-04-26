# tree.py

from dataclasses import dataclass as struct
from dataclasses import field


class Branch(object):
    Edge = "├──"
    Line = "│  "
    Corner = "└──"
    Blank = "   "
    Empty = ""

class Tree(object):
    actions = set('insert delete count paint find traverse tree'.split())
    def __init__(self):
        self.root = None
    def __str__(self):
        data = None
        if self.root:
            data = self.root.data
        return f"Tree(root={data})"
    def count(self):
        dto = DTO()
        if not self.root:
            return 0
        nodes = [self.root]
        count = 0
        while nodes:
            node = nodes.pop(0)
            count += 1
            if node.left:
                nodes.append(node.left)
            if node.right:
                nodes.append(node.right)
        dto.success = True
        dto.messages.append(f"Number of nodes in tree: {count}")
        return dto
    def find(self, x):
        dto = DTO()
        if not self.root:
            dto.success = False
            dto.messages.append(f"Tree is empty. No nodes to search")
            return dto
        temp = self.root
        while temp:
            if x == temp.data:
                dto.success = True
                dto.messages.append(f"Found {x}.")
                dto.data.append(temp)
                return dto
            elif x < temp.data:
                temp = temp.left
            else:
                temp = temp.right
        dto.success = False
        dto.messages.append(f"{x} is not in the tree")
        return dto
    def insert(self, x):
        dto = DTO()
        node = Node(data=x)
        if not self.root:
            self.root = node
            dto.success = self.root is not None
            dto.messages.append(f"Tree is empty. Inserting {x} at root")
            return dto
        temp = self.root
        if temp:
            dto.messages.append(f"Tree is not empty. Starting descent with root")
        while 1:
            dto.messages.append(f"Current node value is {temp.data}")
            smaller = x <= temp.data
            if smaller:
                dto.messages.append(f"{x} is smaller or equal to {temp.data}. Go left.")
                if not temp.left:
                    temp.left = node
                    temp.left.parent = temp
                    dto.messages.append(f"Left is empty. Inserting {x} left of {temp.data}")
                    break
                else:
                    temp = temp.left
                    dto.messages.append(f"Left is not empty. Setting left as current node.")
            else:
                dto.messages.append(f"{x} is larget than {temp.data}. Go right.")
                if not temp.right:
                    temp.right = node
                    temp.right.parent = temp
                    dto.messages.append(f"Right is empty. Inserting {x} right of {temp.data}")
                    break
                else:
                    temp = temp.right
                    dto.messages.append(f"Right is not empty. Setting right as current node.")
        dto.success = True
        return dto
    def traverse(self, style=0):
        dto = DTO()
        if not self.root:
            dto.success = False
            dto.messages.append(f"Tree is empty. No nodes to traverse.")
            return dto
        ordered = []
        if style == 0:
            # preorder
            node = self.root
            exhausted = False
            nodes = []
            while not exhausted:
                if node is not None:
                    nodes.append(node)
                    node = node.left
                else:
                    if nodes:
                        node = nodes.pop()
                        ordered.append(str(node.data))
                        node = node.right
                    else:
                        exhausted = True
        elif style == 1:
            # inorder
            nodes = [self.root]
            while nodes:
                node = nodes.pop(0)
                ordered.append(str(node.data))
                if node.left:
                    nodes.append(node.left)
                if node.right:
                    nodes.append(node.right)
        elif style == 2:
            # postorder
            temp = self.root
            exhausted = False
            nodes = []
            while not exhausted:
                if temp is not None:
                    nodes.append(temp)
                    temp = temp.left
                else:
                    if nodes:
                        temp = nodes.pop()
                        ordered.append(str(temp.data))
                        temp = temp.right
                    else:
                        exhausted = True
        dto.messages.append(" ".join(ordered))
        dto.success = True
        return dto
    def tree(self):
        return DTO()
@struct
class Node:
    data: int = 0
    parent: object = None
    left: object = None
    right: object = None
    def __str__(self):
        return f"Node(data={self.data}, left={self.left}, right={self.right})"

@struct
class DTO:
    success: bool = False
    data: list = field(default_factory=lambda: [])
    messages: list = field(default_factory=lambda: [])
    @property
    def message(self):
        return '\n'.join(self.messages)

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

def main():
    tree = Tree()
    while 1:
        action, *args = input('>>> ').split(' ')
        if action == 'exit':
            break
        valid_action = action in Tree.actions # make sure command is valid
        valid_method = hasattr(Tree, action) # make sure it's implemented
        if not (valid_action and valid_method):
            print("Command not found")
            continue
        command = getattr(tree, action)
        if args:
            request = DTO(data=args)
            response = parse(request)
            if response.message:
                print(response.message)
            if not response.success:
                continue
            for x in response.data:
                response = command(x)
                if response.messages:
                    print(response.message)
        else:
            response = command()
            if response.messages:
                print(response.message) 

if __name__ == "__main__":
    main()
