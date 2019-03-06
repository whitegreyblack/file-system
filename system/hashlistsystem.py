# hashlistsystem.py
from collections import namedtuple
"""
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
# Basically save the group element ids in a hash but hold all elements in a
# list
Ex:
    x = {
        0: (0, 1, 2),
        1: (3, 4),
        2: (5,),
    }

    y = [
        (0, Documents, 1),
        (1, Music, None),
        (2, Folder, 2),
        (3, File, None),
        (4, File, None),
        (5, FIle, None)
        ]
"""

node = namedtuple("Node", "nid gid cid name")
dirsort = lambda x: (x.cid is None, x.name)
dirfilter = lambda l, ns: list(filter(lambda x: x.nid in ns, l))

def print_nodes_indented(d, l, id_dir=0, indent=0):
    nodes = d.get(id_dir, None)
    if nodes is None:
        return
    curdir = dirfilter(l, nodes)
    files_or_folders = sorted(curdir, key=dirsort)
    for file_or_folder in files_or_folders:
        indentation = f"{(' ' * (indent * 4))}"
        print(f"{indentation}{file_or_folder.nid} {file_or_folder.name}")
        print_nodes_indented(d, l, file_or_folder.cid, indent+1)

def print_nodes_full_path(d, l, id_dir=0, path=""):
    nodes = d.get(id_dir, None)
    if nodes is None:
        return
    curdir = dirfilter(l, nodes)
    files_or_folders = sorted(curdir, key=dirsort)
    for file_or_folder in files_or_folders:
        print(f"{file_or_folder.nid} {path + file_or_folder.name}")
        print_nodes_full_path(d, l, file_or_folder.cid, path+file_or_folder.name)

if __name__ == "__main__":
    d = dict()
    d.update({ 0: {0, 1, 2} })
    d.update({ 1: {3, 4, 5} })
    d.update({ 2: {6,} })
    d.update({ 3: {7,} })
    d.update({ 4: {8, 9} })

    l = [
        node(1, 0, 4, "Music/"),
        node(2, 0, None, "File"),
        node(3, 1, None, "File"),
        node(4, 1, 2, "Folder/"),
        node(5, 1, 3, "Directory/"),
        node(6, 2, None, "Text"),
        node(7, 3, None, "Image"),
        node(0, 0, 1, "Documents/"),
        node(8, 4, None, "Playlist"),
        node(9, 4, 5, "Favorites"),
        node(10, 2, None, "Abstract")
    ]

    current_directory_id = 0
    print_nodes_indented(d, l, current_directory_id)
    print_nodes_full_path(d, l, current_directory_id)
