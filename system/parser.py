# parser.py
import os
import yaml
from system.utils import *
"""
Documents:
  - File
  - Folder:
    - Text
  - Directory:
    - Image
Music:
  - Playlist
  - Favorites: []

# After yaml.load():
Since the nodes themselves only hold a name and type, we have to iterate 
through the structure and build the nodes manually. Once they are built
the should be held in a list with nodes(nid, gid, pid, cid, name).

dict(list(dict(list())))

{
    'Documents': [
        'File', 
        { 'Folder': [ 'Text' ] }, 
        { 'Directory': [ 'Image' ] }
    ], 
    'Music': [
        'Playlist', 
        { 'Favorites': [] }
    ]
}

# From yaml, file structure can go into either hashsys, listsys or hashlistsys
# depending on how efficient the structures are. Need time testings to 
# determine which of the three is the most efficient.
"""

filepath = "data" + os.path.sep + "structure.yaml"
node = namedtuple("Node", "nid gid pid cid name")

def read(filepath):
    with open(filepath, 'r') as f:
        return f.read()

def load(filepath):
    with open(filepath, 'r') as f:
        data = f.read()
    return yaml.safe_load(data)

def deserialize_as_list(structure, i=-1, sublevel=0):
    """Returns all nodes in a single list"""
    s, t = [], []
    for k, v in structure.items():
        s.append((k, v, -1, i, '$'))
        i += 1
        while s:
            k, v, l, j, p = s.pop(0)
            if v is not None:
                t.append(node(j, l, p, sublevel, k+"/"))
                if isinstance(v, list):
                    for f in v:
                        if isinstance(f, str):
                            s.append((f, None, sublevel, i, j))
                            i += 1
                        else:
                            for fk, fv in f.items():
                                s.append((fk, fv, sublevel, i, j))
                                i += 1
                sublevel += 1
            else:
                t.append(node(j, l, p, None, k))
    return t

def parse(structure, strategy=deserialize_as_list):
    return strategy(structure)

def serialize_list(data):
    d = dict()
    print(data)

def serialize_hash(data):
    pass

def serialize_hashlist(data):
    pass

def to_hashsys(t):
    max_cid = max(-1 if not n.cid else n.cid for n in t)
    d = dict({ i: dirfilter(t, i) for i in range(max_cid) })
    return d

def to_hashlistsys(t):
    d, l = dict(), list()
    max_cid = max(-1 if not n.cid else n.cid for n in t)
    for i in range(max_cid):
        d[i] = set()
        ns = [n for n in dirfilter(t, i)]
        for n in ns:
            d[i].add(n.nid)
            l.append(n)
    return d, l

if __name__ == "__main__":
    print("# Original File Contents")
    print(read(filepath))
    t = parse(load(filepath))

    print("# Parsed File Contents - Indented Tree")
    print("# NOTE: Ordered by name and folders before files")
    print_inorder_indent_tree(t)
    print()

    print("# Parsed File Contents - Full Path Tree")
    print_inorder_full_path(t)
    print()

    print("# Parsed File Contents - Full Path Tree including folders")
    print_inorder_full_path(t, include_dir=True)

    # d = to_hashsys(t)
    # print(d)
    
    # d, l = to_hashlistsys(t)
    # print(d)
