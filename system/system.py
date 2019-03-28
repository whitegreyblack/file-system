# system.py

import click
import system.parser as parser
import system.utils as utils
from enum import Enum

class Folder(object):
    def __init__(self, name, nid, gid, pid, cid):
        self.name = name
        self.folder_id = nid
        self.directory_id = gid
        self.parent_directory_id = pid
        self.parent_directory = None
        self.child_directory_id = cid
        self.child_directory = None
        self.files_and_folders = list()
    def find_folder(self, foldername):
        for f in self.files_and_folders:
            if isinstance(f, Folder) and f.name == foldername:
                return f
        return None
    def __repr__(self):
        pid = f"{self.parent_directory_id}"
        # gid = f"{self.directory_id}"
        cid = f"{self.child_directory_id}"
        nid = f"{self.folder_id}"
        return f"Folder(nid={nid}, {self.name}, children={len(self.files_and_folders)})"

class File(object):
    def __init__(self, name, nid, gid, pid, reference):
        # self.group_directory_id = gid
        self.file_id = nid
        self.name = name
        self.reference = reference
        self.parent_directory_id = pid

    def __repr__(self):
        pid = f"{self.parent_directory_id}"
        # gid = f"{self.group_directory_id:2}"
        nid = f"{self.file_id}"
        ref = self.reference
        return f"File(nid={nid}, {self.name}, ref={ref})"

# -- system is just a container for holding all files/folders
class System(object):
    """Holds files and folders in a graph structure"""
    class Traversal(Enum):
        preorder = 1
        inorder = 2
        postorder = 3

    def __init__(self, l):
        self.root = None # entry point
        sorted_list = sorted(l, key=lambda n: (n.gid, n.cid is None, n.name))
        for node in sorted_list or []:
            self.insert(node)

    def create_file(self, node):
        return File(node.name, node.gid, node.nid, node.pid, node.ref)

    def create_folder(self, node):
        return Folder(node.name, node.nid, node.gid, node.pid, node.cid)

    def create_system_object(self, node):
        is_file = node.cid == '$'
        return self.create_file(node) if is_file else self.create_folder(node)

    def insert(self, node):
        nodeobj = self.create_system_object(node)
        if not self.root:
            self.root = nodeobj
            return
        index = 0
        stop_iter = False
        current = self.root
        _, *path = node.path[2:].split('/')[:-1]
        # we are at root's sub children
        if not path:
            current.files_and_folders.append(nodeobj)
            return
        # anything below depth of 1 needs recursion
        while current.directory_id != node.pid and path:
            folder = current.find_folder(path.pop(0))
            if not folder:
                break
            current = folder
        current.files_and_folders.append(nodeobj)
                    
    def traverse(self, order=Traversal.preorder):
        if order == self.Traversal.preorder:
            for f in self.preorder():
                yield f
        else:
            yield NotImplemented

    def preorder(self):
        node = self.root
        stack = [node]
        while stack:
            n, *stack = stack
            yield n
            isfolder = isinstance(n, Folder)
            if isfolder:
                stack = [f for f in n.files_and_folders] + stack

@click.command()
@click.argument('filepath', type=click.Path(exists=True))
def main(filepath):
    data = parser.load(filepath)
    nodes = parser.parse(data)
    system = System(nodes)
    print("# Preorder traversal")
    for f in system.traverse():
        print(f)
    print("# Postorder traversal")
    for f in system.traverse(system.Traversal.postorder):
        print(f)

if __name__ == "__main__":
    main()