# objects.py: directory system objects
import itertools
import yaml
import pprint as p
from collections import namedtuple
"""
Directory = {
    # root level = 0
    0: [
        x, y, z
    ],
    # assuming x is a folder, x should be linked to its children by id
    1: [
        a, b, c
    ],
    # assuming y is a folder, y should be linked to its children by id
    2: [
        i, j
    ],
    # assuming z is a file, z should not hold a children id
}
Root:
    - Documents:
        - File
        - Folder:
            - Text
        - Directory:
            - Image
    - Music:
        - Playlist
        - Favorites: []
    - Out_Of_Place_File:

The largest barrier to this implementation is the ability to 'jump' back to
the parent directory. It is not as simple as a parent pointer since the parent
element could be in a folder that needs not only the parent element but also 
horizontal elements that exist in the directory as well.

# visual structures
[Documents, Music, File] (nid: 0, 1, 2), (gid: 0), (pid: None) (cid: 1, 4)
 |          |
 |          +-> [Playlist, Favorites] (id: 8, 9), (gid: 4), (pid: 0), (cid: None)
 |                         |
 |                         +-> [] ()
 |
 +-> [File, Folder, Directory] (id: 3, 4, 5), (gid: 1), (pid: 0), (cid: 2, 3)
            |       |
            |       +-> [Image] (id: 7), (gid: 3), (pid: 1), (cid: None)
            |
            +-> [Text] (id: 6), (gid: 2), (pid: 1), (cid: None)
------
# dictionary structure
{
    0: {
        (nid: 0, gid: 0, pid: !, cid: 1, name: Documents),
        (nid: 1, gid: 0, pid: !, cid: 4, name: Music),
        (nid: 2, gid: 0, pid: !, cid: !, name File)
    },
    1: {
        (nid: 3, gid: 1, pid: 0, cid: !, name: File),
        (nid: 4, gid: 1, pid: 0, cid: 2, name: Folder),
        (nid: 5, gid: 1, pid: 0, cid: 3, name: Directory)
    },
    2: {
        (nid: 6, gid: 2, pid: 1, cid: !, name: Text)
    },
    3: {
        (nid: 7, gid: 3, pid: 1, cid: !, name: Image)
    },
    4: {
        (nid: 8, gid: 4, pid: 0, cid: !, name: Playlist),
        (nid: 9, gid: 4, pid: 0, cid: 5, name; Favorites)
    },
    5: {} # empty directory representation
}

YAML -> Parser => (list | hash) w/ properties -> Tree => Graph

Objects are based on these properties would reflect levels following:
Documents:         # 0 (0, 'Documents')
  - File           # 1 (1, 'File')
  - Folder:        # 1 (1, 'Folder')
    - Text         # 2 (2, 'Text')
  - Directory:     # 1 (1, 'Directory')
    - Image        # 2 (2, 'Image')
Music:             # 0 (0, 'Music')
  - Playlist       # 1 (1, 'Playlist')
  - Favorites: []  # 1 (1, 'Favorites')
Out_Of_Place_File: # 0 (0, 'RootFile')
"""

def flatten(l):
    return list(itertools.chain.from_iterable(l))

class Node(object):
    node_id = 0
    def __init__(self, name, gid, pid, cid):
        self.name = name
        self.node_id = Node.node_id
        self.group_id = pid
        self.parent_id = pid # links to parent group id
        self.children_id = cid # links to children group id

class Parser(object):
    sublevel = -1
    @staticmethod
    def key_or_item(i):
        if isinstance(i, str):
            return i
        if isinstance(i, dict):
            return list(i.keys()).pop()
    @staticmethod
    def parse(d, level=0):
        def subparse(self, level, sublevel):
            pass
        l = []
        Parser.sublevel = max(Parser.sublevel, level+1)
        for key, values in d.items():
            print(f">>> Key:{key}, Val:{[Parser.key_or_item(v) for v in values]}, Lvl: {level}, sub:{Parser.sublevel}")
            children = None
            if isinstance(values, list):
                children = []
                for v in values:
                    print(f">>>>>> Child: {Parser.key_or_item(v)}, Type:{type(v)}")
                    if isinstance(v, str):
                        children.append((v, Parser.sublevel, None))
                    elif isinstance(v, dict):
                        children += Parser.parse(v, Parser.sublevel)
                    print(f">>>>>> Children: {[(c[0], c[1]) for c in children]}")
                    # print("children:", children, '>> sublevel increment: ', Parser.sublevel, "->", Parser.sublevel + 1, '\n')
            print("level", key, level)
            l.append((key, level, children))
        return l

    @staticmethod
    def parse_inorder(d):
        l = []

        for key, values in d.items():
            print(key, values)

class SystemObject(object):
    def __init__(self, name: str, level: int):
        self.name = name
        self.id_level = level
        self.id_children = None
    def __repr__(self):
        return f"SysObj('{self.name}', {self.id_level}, {self.id_children})"
    def connect_children(self, id_children):
        self.id_children = id_children

class Directory(object):
    def __init__(self, sysobjs):
        # always initialize root level
        self.structure = dict({0: set()})
        self.make_tree(sysobjs)

    def add_objects(self, sysobjs: list):
        objects = flatten(sysobjs)
        print(sysobjs, bool(sysobjs))

        if not bool(sysobjs):
            return

        level = self.current_level()
        for obj in sysobjs:
            children = None
            if len(obj) == 2:
                obj, children = obj
            print(level, obj, children)
            sysobj = SystemObject(obj, level)
            self.structure[level].add(sysobj)
            if bool(children):
                self.add_objects(children)
                # sublevel = self.next_level()
                # sysobj.connect_children(sublevel)
                # for child in children:
                #     sysobj = SystemObject(obj, sublevel)
                #     self.structure[sublevel].add(child)  
        p.pprint(self.structure)

    def make_tree(self, sysobjs):
        print(sysobjs, bool(sysobjs), '\n')

        if not bool(sysobjs):
            return

        level = 0
        sublevel = 1
        l = [(k, v, level) for k, v in sysobjs.items()]
        while l:
            k, vs = l.pop(), None
            print(k)
            if len(k) == 3:
                k, vs, lvl = k
            if vs == None:
                vs = []
            sysobj = SystemObject(k, lvl)
            for v in vs:
                if isinstance(v, str):
                    l.append((v, None, sublevel))
                if isinstance(v, dict):
                    for k, v in v.items():
                        l.append((k, v, sublevel))
            sublevel += 1
        for k, v in self.structure.items():
            print(k, v)

    def current_level(self) -> int:
        # return last used level id
        if not bool(self.structure):
            return 0
        return max(self.structure.keys())

    def next_level(self) -> int:
        # initialize the next level id
        next = self.current_level() + 1
        self.structure[next] = set()
        return next

class Folder(object):
    def __init__(self, parent, name, files):
        self.name = name
        self.files = []
        
        for f in files:
            pass

"""
Try an index-based array directory
[
    [0, x]
    [1, a]
    [1, b]
    [2, i]
    [0, y]
    [0, z]
]
"""

if __name__ == "__main__":
    data = [
        ("Documents", [
            "File.txt",
            # ("Projects", [
            #     # "File1.png",
            #     # "File2.txt",
            # ]),
            # ("Games", []),
        ]),
        ("Music", []),
        # ("Pictures", []),
        # ("Desktop", [
        #     ("Stuff", [])
        # ]),
        "Out_Of_Place_File.txt",
    ]
    with open("examples/system/structure.yaml", "r") as f:
        filedata = f.read()
    data = yaml.load(filedata)
    # d = Directory(data)
    # Parser.parse_inorder(data)
    # parsed = Parser.parse(data)
    # print(parsed)
    # for i in parsed:
    #     print(i[1::-1])
    #     c = i[2]
    #     if c:
    #         for j in c:
    #             p.pprint(j[1::-1])
    #             d = j[2]
    #             if d:
    #                 for k in d:
    #                     print(k[1::-1])
    # print(list(itertools.chain.from_iterable(list(data))))
    # d = Directory(data)


    print(data);

    root = Folder(None, "Root", data)
    for i, c in data.items():
        print(i)
