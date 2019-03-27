# systems.py

import click
import system.parser as parser
import system.tree as tree
import system.utils as utils

class Folder(object):
    def __init__(self, name, nid, gid, pid, cid):
        self.name = name
        self.folder_id = nid
        self.directory_id = gid
        self.parent_directory_id = pid
        self.parent_directory = None
        self.child_directory_id = cid
        self.child_directory = None
        self.files_and_folders = list()
    def find_folder(self, foldername):
        print('find ', foldername)
        for f in self.files_and_folders:
            if isinstance(f, Folder) and f.name == foldername:
                return f
        return None
    def __repr__(self):
        pid = self.parent_directory_id
        gid = self.directory_id
        cid = self.child_directory_id
        nid = self.folder_id
        return f"Folder({self.name}, nid={nid} pid={pid}, gid={gid}, cid={cid})"

class File(object):
    def __init__(self, name, nid, gid, pid, reference):
        # self.group_directory_id = dirid
        self.group_directory = None
        self.group_directory_id = -1
        self.file_id = nid
        self.name = name
        self.reference = reference
        self.parent_directory_id = -1

    def __repr__(self):
        pid = self.parent_directory_id
        gid = self.group_directory_id
        nid = self.file_id
        ref = self.reference
        return f"File({self.name}, nid={nid} pid={pid}, gid={gid}, ref={ref})"

# -- system is just a container for holding all files/folders
class System(object):
    def __init__(self, l):
        self.root = None # entry point
        sorted_list = sorted(l, key=lambda n: (n.gid, n.cid is None, n.name))
        for node in sorted_list or []:
            self.insert(node)

    def create_file(self, node):
        return File(node.name, node.gid, node.nid, node.pid, node.ref)

    def create_folder(self, node):
        return Folder(node.name, node.nid, node.gid, node.pid, node.cid)

    def create_system_object(self, node):
        is_file = node.cid == '$'
        return self.create_file(node) if is_file else self.create_folder(node)

    def insert(self, node):
        print('insert')
        nodeobj = self.create_system_object(node)
        if not self.root:
            self.root = nodeobj
        else:
            index = 0
            stop_iter = False
            current = self.root
            _, *path = node.path[2:].split('/')[:-1]
            if not path:
                current.files_and_folders.append(nodeobj)
                return

            print(path)
            while current.directory_id != node.pid and path:
                folder = current.find_folder(path.pop())
                print('>>>',folder)
            current.files_and_folders.append(nodeobj)
            # exit()

            # while not stop_iter:
            #     print(node.name, current.files_and_folders, current.directory_id, node.gid, node.pid)
            #     for n in current.files_and_folders:
            #         print(n.name, path_stops[index])
            #         if n.name == path_stops[index]:
            #             current = n.child_directory
            #             index += 1
            #         exit()
            #         break
            #     if current.directory_id == node.pid:
            #         print('match', current.directory_id, node.pid)
            #         stop_iter = True
            # current.files_and_folders.append(nodeobj)
            # while paths:
            #     path, *paths = paths
            #     if path == current.name:
                    

    def traversal(self):
        node = self.root
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
                ] + nodess

@click.command()
@click.argument('filepath', type=click.Path(exists=True))
def main(filepath):
    stack = parser.load(filepath)
    l = parser.parse(stack)
    utils.print_inorder(l)
    utils.print_inorder_indent_tree(l)
    s = System(l)
    print(s.root)
    print(s.root.files_and_folders)
    for n in s.root.files_and_folders:
        print(n)

if __name__ == "__main__":
    main()