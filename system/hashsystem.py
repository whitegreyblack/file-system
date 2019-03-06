# hashsystem.py
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
"""

node = namedtuple("Node", "nid gid pid cid name")
dirsort = lambda x: (x.cid is None, x.name)

def print_nodes_indented(d, id_dir=0, indent=0):
    curdir = d.get(id_dir, None)
    if curdir is None:
        return
    for file_or_folder in sorted(curdir, key=dirsort):
        indentation = f"{(' ' * (indent * 4))}"
        print(f"{indentation}{file_or_folder.nid} {file_or_folder.name}")
        print_nodes_indented(d, file_or_folder.cid, indent+1)

def print_nodes_full_path(d, id_dir=0, path=""):
    curdir = d.get(id_dir, None)
    if curdir is None:
        return
    for file_or_folder in sorted(curdir, key=dirsort):
        print(f"{file_or_folder.nid} {path + file_or_folder.name}")
        print_nodes_full_path(d, file_or_folder.cid, path+file_or_folder.name)

if __name__ == "__main__":
    d = dict({ i: set() for i in range(6) })
    d[0].add(node(1, 0, None, 4, "Music/"))
    d[0].add(node(0, 0, None, 1, "Documents/"))
    d[0].add(node(2, 0, None, None, "File"))
    d[1].add(node(3, 1, 0, None, "File"))
    d[1].add(node(4, 1, 0, 2, "Folder/"))
    d[1].add(node(5, 1, 0, 3, "Directory/"))
    d[2].add(node(6, 2, 1, None, "Text"))
    d[2].add(node(10, 2, 1, None, "Abstract"))
    d[3].add(node(7, 3, 1, None, "Image"))
    d[4].add(node(8, 4, 0, None, "Playlist"))
    d[4].add(node(9, 4, 0, 5, "Favorites/"))

    current_directory_id = 0
    print_nodes_indented(d, current_directory_id)
    print_nodes_full_path(d, current_directory_id)
