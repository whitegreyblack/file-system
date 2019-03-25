# tree.py
"""
Takes in a list of file nodes and creates a tree.
"""
import system.utils as utils

class Directory(object):
    def __init__(self, gid, pid):
        self.group_directory_id = gid
        self.parent_directory_id = pid
        self.files_and_folders = list()

class File(object):
    def __init__(self, name, dirid, nid, reference):
        self.group_directory_id = dirid
        self.group_directory = None
        self.file_id = nid
        self.name = name
        self.reference = reference
    def __repr__(self):
        return "Folder"  

class Folder(object):
    def __init__(self, name, dirid, nid, cid):
        self.group_directory_id = dirid
        self.group_directory = None
        self.folder_id = nid
        self.name = name
        self.child_directory_id = cid
        self.child_directory = Directory(cid, dirid)
    
    def __repr__(self):
        return f"""
Folder {self.name}:
> Paren DIR: {self.group_directory.parent_directory_id}
> Group DIR: {self.group_directory_id}
> Child DIR: {self.child_directory_id}
"""[1:]

class System(object):
    def __init__(self, l):
        self.rootdir = None
        sorted_list = sorted(l, key=lambda n: (n.gid, n.cid is None, n.name))
        print("N G P C Name\n------------")
        for node in sorted_list or []:
            # print(utils.el_repr(node))
            self.insert(node)
        print("done inserting")

    def create_file(self, node):
        return File(node.name, node.gid, node.nid, node.ref)

    def create_folder(self, node):
        return Folder(node.name, node.gid, node.nid, node.cid)

    def create_system_object(self, node):
        is_file = node.cid == '$'
        return self.create_file(node) if is_file else self.create_folder(node)

    def insert(self, node):
        nodeobj = self.create_system_object(node)
        if not self.rootdir:
            nodedir = Directory(node.gid, '$')
            nodeobj.group_directory = nodedir
            nodedir.files_and_folders.append(nodeobj)
            self.rootdir = nodedir
        else:
            current = self.rootdir
            if current.group_directory_id == node.gid:
                nodeobj.group_directory = current
                current.files_and_folders.append(nodeobj)
            else:
                path_stops = node.path[2:].split('/')
                print(path_stops)
                print('Gid: ', node.gid)
                stop_iter = False
                while not stop_iter:
                    print("current group id:", current.group_directory_id)
                    for n in current.files_and_folders:
                        if n.name in node.path:
                            print(n.name, node.path)
                            current = n.child_directory
                            break
                    if current.group_directory_id == node.gid:
                        stop_iter = True
                print(current.group_directory_id)
                nodeobj.group_directory = current
                current.files_and_folders.append(nodeobj)

    def traversal(self):
        node = self.rootdir
        print('traversal')
        nodes = [x for x in node.files_and_folders]
        while nodes:
            n, *nodes = nodes
            print(n.name)
            if isinstance(n, Folder):
                nodes = [x for x in n.child_directory.files_and_folders] + nodes

    def size(self):
        return get_number_of_objects_in_dir()

if __name__ == "__main__":
    import system.parser as parser
    from collections import namedtuple
    import os

    filepath = "." + os.path.sep + "data" + os.path.sep + "mini.yaml"
    l = parser.parse(parser.load(filepath))
    s = System(l)
    s.traversal()