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
    actions = set('insert balance delete count paint find traverse tree inorder preorder postorder'.split())
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
            return dto
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
        """TODO: implement balancing after insert"""
        dto = DTO()
        if not self.root:
            self.root = Node(data=x)
            dto.success = self.root is not None
            dto.messages.append(f"Tree is empty. Inserting {x} at root")
            return dto
        temp = self.root
        if temp:
            dto.messages.append(f"Tree is not empty. Starting descent with root")
        while 1:
            dto.messages.append(f"Current node value is {temp.data}")
            if x == temp.data:
                temp.count += 1
                dto.messages.append(f"{x} already exists in the tree. Incrementing count")
                break
            elif x < temp.data:
                dto.messages.append(f"{x} is smaller or equal to {temp.data}. Go left.")
                if not temp.left:
                    temp.left = Node(data=x)
                    temp.left.parent = temp
                    dto.messages.append(f"Left is empty. Inserting {x} left of {temp.data}")
                    break
                else:
                    temp = temp.left
                    dto.messages.append(f"Left is not empty. Setting left as current node.")
            else:
                dto.messages.append(f"{x} is larget than {temp.data}. Go right.")
                if not temp.right:
                    temp.right = Node(data=x)
                    temp.right.parent = temp
                    dto.messages.append(f"Right is empty. Inserting {x} right of {temp.data}")
                    break
                else:
                    temp = temp.right
                    dto.messages.append(f"Right is not empty. Setting right as current node.")
        dto.success = True
        return dto
    def traverse(self, style=1):
        dto = DTO()
        if not self.root:
            dto.success = False
            dto.messages.append(f"Tree is empty. No nodes to traverse.")
            return dto
        if style == 0:
            traversal = self.preorder
        elif style == 1:
            traversal = self.inorder
        elif style == 2:
            traversal = self.postorder
        return response()
    def inorder(self):
        dto = DTO()
        if not self.root:
            dto.success = False
            dto.messages.append(f"Tree is empty. No nodes to traverse.")
            return dto
        node = self.root
        exhausted = False
        nodes = []
        ordered = []
        while not exhausted:
            if node is not None:
                nodes.append(node)
                node = node.left
            else:
                if nodes:
                    node = nodes.pop()
                    ordered.append(node)
                    node = node.right
                else:
                    exhausted = True
        dto.success = bool(ordered)
        if dto.success:
            dto.data = ordered
            dto.messages.append(" ".join(str(d.data) for d in ordered))
        return dto
    def preorder(self):
        dto = DTO()
        if not self.root:
            dto.success = False
            dto.messages.append(f"Tree is empty. No nodes to traverse.")
            return dto

        ordered = []
        nodes = [self.root]
        while nodes:
            node = nodes.pop(0)
            ordered.append(str(node.data))
            if node.left:
                nodes.append(node.left)
            if node.right:
                nodes.append(node.right)
        dto.success = bool(ordered)
        if dto.success:
            dto.data = ordered
            dto.messages.append(" ".join(str(d) for d in ordered))
        return dto
    def postorder(self):
        dto = DTO()
        if not self.root:
            dto.success = False
            dto.messages.append(f"Tree is empty. No nodes to traverse.")
            return dto
        ordered = []
        node = self.root
        exhausted = False
        nodes = [self.root]
        while nodes:
            node = nodes.pop()
            ordered.append(str(node.data))
            if node.left:
                nodes.append(node.left)
            if node.right:
                nodes.append(node.right)
        dto.data = ordered[::-1]
        dto.success = bool(ordered)
        return dto
    def balance(self):
        dto = DTO()
        if not self.root:
            dto.success = False
            dto.messages.append(f"Tree is empty. Cannot balance empty tree.")
            return dto
        response = self.inorder()
        if not response.success:
            return response
        self.root = None
        l, m, r = 0, len(response.data) // 2, len(response.data)
        nodes = [response.data[m]]
        ordered = []
        while nodes:
            node = nodes.pop(0)
            print(node)
            self.insert(node.data)
            left = response.data[l:m]
            if left:
                l, m, r = 0, len(left) // 2, len(left)
                nodes.append(response.data[m])
        print(ordered)

        """
        self.root = None
        # insert root node
        inserted = self.insert(response.data[mid].data)
        left = response.data[:mid]
        while left:
            m = len(left) // 2
            self.insert(response.data[m].data)
            left = left[:m]
        """ 

        return DTO()
    def tree(self):
        return DTO()
@struct
class Node:
    data: int = 0
    count: int = 1
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
    """TODO: cache last result only"""
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
