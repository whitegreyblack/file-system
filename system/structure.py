# structure.py
import random
from collections import namedtuple
import click
from system.tree import Directory, Folder, File, System, Tree
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
node = namedtuple("Node", "nid gid pid cid name path ref")

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

def build_structure(count=100):
                 "nid gid pid cid name path ref"
    nodes = [node(0, 0, '$', 1, 'Root', '~/', '$')]
    s = System(nodes)
    for n in Tree.grow(s):
        print(n)
    cutoff = 1.0
    max_depth = 10
    current_nid = 1
    current_level = 1
    current_parent = 1
    while bool(count):
        if random.random() < cutoff:
            n = node(current_nid, current_level, current_parent)
    
    print_inorder(l)
    print_inorder_indent_tree(l)

    return "system\structure.yaml"

@click.command()
@click.argument('filepath', type=click.Path())
def main(filepath):
    # handle user input on using file that already exists
    try:
        with open(filepath, 'r') as f:
            pass
    except FileNotFoundError:
        pass
    finally:
        answer = input(f"File on path: {filepath} already exists. Overwrite file (Y/N)?: ")
        overwrite = answer.lower() == "y"
        if not overwrite:
            print("Exitting early. Run program with a different file path.")

    # build file system
    build_structure()

if __name__ == "__main__":
    main()
    # filename = build_structure()
    # with open(filename, 'r') as f:
    #     print(f.read())
