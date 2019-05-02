# tree.py

from models import Branch, DTO, Node
import random

class Tree(object):
    def __init__(self):
        self.root = None

    def __str__(self):
        data = None
        if self.root:
            data = self.root.data
        return f"Tree(root={data})"

    def new(self):
        self.root = None 
        return DTO(messages=["Tree was cut down"], success=True)

    def cut(self, x):
        dto = DTO()
        response = self.find(x)
        dto.extend(response)
        if not dto.success:
            dto.messages.append(f"Aborting cut.")
            return dto
        # it is known now that node exists. cut it out
        if x == self.root.data:
            response = self.new()
            dto.extend(response)
            return dto
        temp = self.root
        while temp:
            if x == temp.data:
                temp = None
            elif x < temp.data:
                if temp.left and temp.left.data != x:
                    temp = temp.left
                else:
                    temp.left = None
                    temp = temp.left
            else:
                if temp.right and temp.right.data != x:
                    temp = temp.right
                else:
                    temp.right = None
                    temp = temp.right

        dto.messages.append(f"Cutting branch.")
        dto.success = not self.find(x).success
        return dto

    def random(self, x):
        l = list(range(x))
        random.shuffle(l)
        return DTO(success=True, data=l)

    def randrange(self, start, end):
        self.rand_beg = start
        self.rand_end = end + 1

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
        return traversal()

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
                    ordered.append(node.data)
                    node = node.right
                else:
                    exhausted = True
        dto.success = bool(ordered)
        if dto.success:
            dto.data = ordered
            dto.messages.append(" ".join(str(d) for d in ordered))
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
            ordered.append(node.data)
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
        nodes = []
        node = self.root
        exhausted = False
        while not exhausted:
            while node:
                if node.right:
                    nodes.append(node.right)
                nodes.append(node)
                node = node.left
            node = nodes.pop()
            if node.right and nodes[-1] == node.right:
                nodes.pop()
                nodes.append(node)
                node = node.right
            else:
                ordered.append(node.data)
                node = None
            if not nodes:
                exhausted = True
        dto.success = bool(ordered)
        if dto.success:
            dto.data = ordered[::-1]
            dto.messages.append(" ".join(str(d) for d in ordered))
        return dto
    
    def balanced(self):
        return False

    def balance(self, node=None):
        dto = DTO()
        if not self.root:
            dto.success = False
            dto.messages.append(f"Tree is empty. Cannot balance empty tree.")
            return dto
        if self.balanced():
            dto.success = False
            dto.messages.append(f"Tree is already balanced. Returning early")
            return dto
        response = self.inorder()
        if not response.success:
            dto.message.append(f"Inorder returned unsuccessful. Exitting balance early")
            return dto
        # don't clear out tree yet. need to find the correct ordering from data
        # nodes = [response.data[m]] # holds correct ordering for insertion
        ordered = []
        slices = [response.data]
        while slices:
            nodes = slices.pop(0)
            m = len(nodes) // 2
            ordered.append(nodes[m])
            left, right = nodes[:m], nodes[m+1:]
            if left:
                slices.append(left)
            if right:
                slices.append(right)
        # now clear out root
        self.new()
        for i in ordered:
            response = self.insert(i)
            dto.messages.extend(response.messages)

        dto.data = ordered
        dto.success = bool(ordered)
        dto.messages.append(' '.join(str(d) for d in ordered))
        return dto

    def tree(self, node=None):
        dto = DTO()
        if not self.root:
            dto.success = False
            dto.messages.append("Tree is empty")
            return dto
        if node:
            response = self.find(node)
            if not response.success:
                dto.extend(response)
                return dto
            node = response.data.pop()
        else:
            node = self.root
        depth = 0
        count, leaves = 0, 0
        nodes = [(node, True, depth, Branch.Empty)]
        while nodes:
            (node, last, depth, prefix), *nodes = nodes
            count += 1
            if not node.leaf:
                prefix_add = ""
                if depth > 0:
                    prefix_add = Branch.Blank if last else Branch.Line
                if node.left and node.right:
                    nodes.insert(0, (node.left, True, depth + 1, prefix + prefix_add))
                    nodes.insert(0, (node.right, False, depth + 1, prefix + prefix_add))
                elif node.right:
                    nodes.insert(0, (node.right, True, depth + 1, prefix + prefix_add))
                else:
                    nodes.insert(0, (node.left, True, depth + 1, prefix + prefix_add))
            else:
                leaves += 1
            branch = ""
            if depth > 0:
                branch = Branch.Corner if last else Branch.Edge
            dto.messages.append(f"{prefix}{branch}{node.data}")
            if not nodes:
                break
        dto.messages.append(f"Nodes: {count}, Leaves: {leaves}")
        return dto

Tree.actions = set(fn for fn in dir(Tree) if callable(getattr(Tree, fn)) and not fn.startswith('__'))

if __name__ == "__main__":
    print("Usage: py .")

