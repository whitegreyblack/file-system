# parser.py
import os
import yaml
import click
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
        { 'File': 'data/file' }, 
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
node = namedtuple("Node", "nid gid pid cid name")

def read(filepath):
    with open(filepath, 'r') as f:
        return f.read()

def load(filepath):
    return yaml.safe_load(read(filepath))

def deserialize_copy(structure):
    t = []
    level = 1
    nodeid = 1
    # start with root node. all nodes will fall under this
    s = [('Root', structure, 0, 0, '$', '~/', '$')]
    node = namedtuple("Node", "nid gid pid cid name path ref")

    while s:
        ref = '$'
        cid = level
        n = s.pop(0)
        name, children, gid, nid, pid, path, ref = n
        if isinstance(children, str):
            cid = '$'
            ref = children
        elif isinstance(children, dict):
            for cname, cchild in children.items():
                cpath = f"{path}{name}/"
                s.append((cname, cchild, level, nodeid, gid, cpath, '$'))
                nodeid += 1
            level += 1
        else:
            level += 1
        t.append(node(nid, gid, pid, cid, name, path, ref))
    return t

def parse(structure, strategy=deserialize_copy):
    return strategy(structure)

def serialize_list(data):
    d = dict()
    print(data)

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

@click.command()
@click.argument('filepath', type=click.Path(exists=True))
def main(filepath):
    import pprint
    # filepath = "data" + os.path.sep + filename

    # print("# Original File Contents")
    # print(read(filepath))
    pprint.pprint(load(filepath))
    t = parse(load(filepath))
    print("# Node list: ")
    for i in t:
        print(i)
    print()

    print("# Parsed File Contents - Indented Tree")
    print("# NOTE: Ordered by name and folders before files")
    print_inorder_indent_tree(t)
    print()

    print("# Parsed File Contents - Full Path Tree")
    print_inorder_full_path(t)
    print()
    print("# Parsed File Contents - Full Path Tree with Refs")
    print_inorder_full_path(t, include_ref=True)
    print()
    # print("# Parsed File Contents - Full Path Tree including folders")
    # print_inorder_full_path(t, include_dir=True)

    print("# Print Inorder")
    print_inorder(t)
    print()

    print("# Print Preorder")
    print_inorder(t, sort=dirsortid)


if __name__ == "__main__":
    main()
    