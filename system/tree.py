# tree.py
"""
Takes in a list of file nodes and creates a tree.
"""

class File(object):
    def __init__(self, name, pid):
        self.parent_directory_id = pid
        self.name = name

class Folder(object):
    def __init__(self, name, pid, gid, level):
        self.parent_directory_id = pid
        self.group_id = gid
        self.links = dict()
        self.items = set()
        self.level = level
        self.name = name
        
    def add_file_or_folder(self, item):
        self.items.add(item)

class System(object):
    def __init__(self, l=None):
        # entry point
        self.root = Folder("Root", None, 0, 0)
        
        if l:
            sorted_l = sorted(l, key=lambda n: (n.gid, n.cid is None, n.name))
            for n in sorted_l:
                print(n.name)
                self.insert(n)

    def insert(self, sysobj):
        if self.root is None:
            n = Folder(sysobj.name, sysobj.pid, sysobj.gid, 0)
            n.add_file_or_folder(sysobj)
            self.root = n
        else:
            current = self.root

    def print_system(self):
        nodes = list(self.root.items)
        print(nodes)

if __name__ == "__main__":
    import system.parser as parser
    from collections import namedtuple
    import os

    filepath = "." + os.path.sep + "data" + os.path.sep + "structure.yaml"
    l = parser.parse(parser.load(filepath))
    s = System(l)
