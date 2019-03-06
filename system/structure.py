# structure.py
import random
from collections import namedtuple

from system import *
"""
Could also be named [generate.py] (maybe)
Main idea for this class is to build a similar structure not unlike below:
---
structure.yaml:
    Documents:
    - File
    - Folder:
        - Text
    - Directory:
        - Image
    Music:
    - Playlist
    - Favorites: []
---
One method will be build(n=10) where n is total number of nodes in the structure.
So once build(n) it should return a string that indicates the file name of the 
completed system structure in correct yaml syntax.

Maybe once classes are built instead we can randomly generate a yaml file off
of a randomly built class.

"""
node = namedtuple("Node", "nid gid pid cid name")

def generate_json_from_nodes(l):
    d = dict()
    return d

def build_random_node(nid, gid):
    pid = None
    if gid != 0:
        pid = random.randint(0, gid-1)
    name = random_file_name() * random.randint(6, 12)
    cid = None
    if bool(random.getrandbits(1)):
        name = random_folder_name() * random.randint(6, 12) + "/"
        cid = gid + random.randint(0, 5)
    return node(nid, gid, pid, cid, name)

def build_structure(nodes=100):
    l = []
    max_gid = 0
    for i in range(nodes):
        n = build_random_node(i, random.randint(0, max_gid+1))
        max_gid = max(n.gid, max_gid)
        l.append(n)
    
    print_inorder(l)
    print_inorder_indent_tree(l)

    return "system\structure.yaml"

if __name__ == "__main__":
    filename = build_structure()
    with open(filename, 'r') as f:
        print(f.read())
