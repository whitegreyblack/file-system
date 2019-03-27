# tree.py
"""
Takes in a list of file nodes and creates a tree.
"""
import click
import system.utils as utils
import system.parser as parser
from collections import namedtuple
from datetime import datetime
import os

class Tree(object):
    Edge = "├──"
    Line = "│  "
    Corner = "└──"
    Blank = "   "
    Empty = ""
    @staticmethod
    def grow(directory):
        """Print directory tree"""
        depth = 0
        size = len(directory.rootdir.files_and_folders)
        stack = [
            (f, i, depth, size, Tree.Empty) 
                for i, f in enumerate(directory.rootdir.files_and_folders)
        ]
        while stack:
            # d determines indentation level
            # l determines which tree string to use on print
            (f, i, d, l, p), *stack = stack
            folder = isinstance(f, Folder)
            if folder:
                nid = f"{f.folder_id:>2}"
                cid = f"{f.child_directory_id:>2}"
            else:
                nid = f"{f.file_id:>2}"
                cid = f"{'$':>2}"
            gid = f"{f.group_directory_id:>2}"
            pid = f"{f.group_directory.parent_directory_id:>2}"

            link = ""
            if d > 0:
                link = Tree.Corner if i == l-1 else Tree.Edge
            noderow = f"{nid} {gid} {pid} {cid} {p}{link}{f.name}"
            if not folder:
                noderow += f" => {f.reference}"
            yield noderow

            if folder:
                childdir = f.child_directory.files_and_folders
                size = len(childdir)
                # break early if no children nodes in the directory
                if size == 0:
                    continue
                
                prefix = ""
                # level under root never has lines
                if d > 0:
                    prefix = p + Tree.Line
                    if i == l-1:
                        prefix = p + Tree.Blank
                nodes = [
                    (f, i, d+1, size, prefix) for i, f in enumerate(childdir)
                ]
                # add to front of the stack
                stack = nodes + stack


class Directory(object):
    dirid = 1
    def __init__(self, gid, pid):
        self.group_directory_id = gid
        self.parent_directory_id = pid
        self.files_and_folders = list()
        self.modified_date = datetime.now()
        self.created_date = datetime.now()
    def update_last_modified_date(self):
        self.last_modified_date = max(
            lambda x: x.last_modified_date, 
            self.files_and_folders
        )
    def __repr__(self):
        gid = self.group_directory_id
        return f"Directory(gid={gid})"


class Folder(object):
    def __init__(self, name, dirid, nid, cid):
        self.group_directory_id = dirid
        self.group_directory = None
        self.folder_id = nid
        self.name = name
        self.child_directory_id = cid
        self.child_directory = Directory(cid, dirid)
        self.modified_date = datetime.now()
        self.created_date = datetime.now()
    def __repr__(self):
        pid = self.group_directory.parent_directory_id
        gid = self.group_directory_id
        cid = self.child_directory_id
        nid = self.folder_id
        return f"Folder({self.name}, nid={nid} pid={pid}, gid={gid}, cid={cid})"


class File(object):
    def __init__(self, name, dirid, nid, reference):
        self.group_directory_id = dirid
        self.group_directory = None
        self.file_id = nid
        self.name = name
        self.reference = reference
        self.modified_date = datetime.now()
        self.created_date = datetime.now()

    def __repr__(self):
        pid = self.group_directory.parent_directory_id
        gid = self.group_directory_id
        nid = self.file_id
        ref = self.reference
        return f"File({self.name}, nid={nid} pid={pid}, gid={gid}, ref={ref})"


class System(object):
    def __init__(self, l):
        self.rootdir = None
        sorted_list = sorted(l, key=lambda n: (n.gid, n.cid is None, n.name))
        for node in sorted_list or []:
            self.insert(node)

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
            index = 0
            stop_iter = False
            current = self.rootdir
            path_stops = node.path[2:].split('/')[:-1]
            while not stop_iter:
                for n in current.files_and_folders:
                    if n.name == path_stops[index]:
                        current = n.child_directory
                        index += 1
                        break
                if current.group_directory_id == node.gid:
                    stop_iter = True
            nodeobj.group_directory = current
            current.files_and_folders.append(nodeobj)

    def traversal(self):
        node = self.rootdir
        nodes = [(node.group_directory_id, x) for x in node.files_and_folders]
        while nodes:
            n, *nodes = nodes
            gid, n = n
            yield n
            if isinstance(n, Folder):
                child_dir = n.child_directory
                nodes = [
                    (child_dir.group_directory_id, x) 
                        for x in child_dir.files_and_folders
                ] + nodes

    def size(self):
        return get_number_of_objects_in_dir()


@click.command()
@click.argument('filepath', type=click.Path(exists=True))
def main(filepath):
    stack = parser.load(filepath)
    l = parser.parse(stack)
    s = System(l)
    for n in Tree.grow(s):
        print(n)

if __name__ == "__main__":
    main()