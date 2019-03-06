# listsystem.py
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
[
    (nid: 0, gid: 0, pid: !, cid: 1, name: Documents),
    (nid: 1, gid: 0, pid: !, cid: 4, name: Music),
    (nid: 2, gid: 0, pid: !, cid: !, name File),
    (nid: 3, gid: 1, pid: 0, cid: !, name: File),
    (nid: 4, gid: 1, pid: 0, cid: 2, name: Folder),
    (nid: 5, gid: 1, pid: 0, cid: 3, name: Directory),
    (nid: 6, gid: 2, pid: 1, cid: !, name: Text),
    (nid: 7, gid: 3, pid: 1, cid: !, name: Image),
    (nid: 8, gid: 4, pid: 0, cid: !, name: Playlist),
    (nid: 9, gid: 4, pid: 0, cid: 5, name; Favorites)
]
"""

node = namedtuple("Node", "nid gid pid cid name")
dirsort = lambda x: (x.cid is None, x.name)
dirfilter = lambda l, i: list(filter(lambda n: n.gid == i, l))

def print_nodes_indented(l, id_dir=0, indent=0):
    if id_dir == None:
        return
    curdir = dirfilter(l, id_dir)
    if not curdir:
        return
    files_or_folders = sorted(curdir, key=dirsort)
    for file_or_folder in files_or_folders:
        indentation = f"{(' ' * (indent * 4))}"
        print(f"{indentation}{file_or_folder.nid} {file_or_folder.name}")
        print_nodes_indented(l, file_or_folder.cid, indent+1)

def print_nodes_full_path(l, id_dir=0, path=""):
    if id_dir == None:
        return
    curdir = dirfilter(l, id_dir)
    if not curdir:
        return
    files_or_folders = sorted(curdir, key=dirsort)
    for file_or_folder in files_or_folders:
        print(f"{file_or_folder.nid} {path + file_or_folder.name}")
        print_nodes_full_path(l, file_or_folder.cid, path+file_or_folder.name)

if __name__ == "__main__":
    l = [
        node(1, 0, None, 4, "Music/"),
        node(0, 0, None, 1, "Documents/"),
        node(2, 0, None, None, "File"),
        node(3, 1, 0, None, "File"),
        node(4, 1, 0, 2, "Folder/"),
        node(5, 1, 0, 3, "Directory/"),
        node(6, 2, 1, None, "Text"),
        node(10, 2, 1, None, "Abstract"),
        node(7, 3, 1, None, "Image"),
        node(8, 4, 0, None, "Playlist"),
        node(9, 4, 0, 5, "Favorites/")
    ]

    current_directory_id = 0
    current_directory = dirfilter(l, current_directory_id)
    print_nodes_indented(l, current_directory_id)
    print_nodes_full_path(l, current_directory_id)
