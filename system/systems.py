# systems.py

import click
import system.parser as parser
import system.utils as utils

class Tree (object):
    Edge = "├──"
    Line = "│  "
    Corner = "└──"
    Blank = "   "
    Empty = ""
    @staticmethod
    def newgrow(filesystem):
        stack = [(filesystem.root, 0, 0, 1, Tree.Empty)]
        while stack:
            (f, i, d, s, p), *stack = stack
            folder = isinstance(f, Folder)
            # print(f.name, 'isfolder', folder, type(f))
            if folder:
                nid = f"{f.folder_id:2}"
                cid = f"{f.child_directory_id:2}"
            else:
                nid = f"{f.file_id:2}"
                cid = f"{'$':>2}"
            # gid = f"{f.directory_id:>2}"
            pid = f"{f.parent_directory_id:>2}"

            link = ""
            if d > 0:
                link = Tree.Corner if i == s-1 else Tree.Edge
            noderow = f"{nid} {pid} {cid} {p}{link}{f.name}"
            if not folder:
                noderow += f" => {f.reference}"
            yield noderow

            if folder:
                size = len(f.files_and_folders)
                if size == 0:
                    continue
                prefix = ""
                if d > 0:
                    prefix = p + Tree.Line
                    if i == s-1:
                        prefix = p + Tree.Blank
                nodes = [
                    (f, i, d+1, size, prefix) for i, f, in
                        enumerate(f.files_and_folders)
                ]
                stack = nodes + stack            
            if not stack:
                break

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
                print('found', f.name)
                return f
        return None
    def __repr__(self):
        pid = f"{self.parent_directory_id:2}"
        gid = f"{self.directory_id}"
        cid = f"{self.child_directory_id}"
        nid = f"{self.folder_id}"
        return f"F(nid={nid} pid={pid}, gid={gid}, cid={cid}, {self.name})"

class File(object):
    def __init__(self, name, nid, gid, pid, reference):
        self.group_directory_id = gid
        self.file_id = nid
        self.name = name
        self.reference = reference
        self.parent_directory_id = pid

    def __repr__(self):
        pid = f"{self.parent_directory_id:2}"
        gid = f"{self.group_directory_id:2}"
        nid = f"{self.file_id:2}"
        ref = self.reference
        return f"f(nid={nid}, pid={pid}, gid={gid}, {self.name}, ref={ref})"

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
        nodeobj = self.create_system_object(node)
        if not self.root:
            print('insert root')

            self.root = nodeobj
        else:
            print('insert subroot', node.name)
            index = 0
            stop_iter = False
            current = self.root
            _, *path = node.path[2:].split('/')[:-1]
            # we are at root's sub children
            if not path:
                current.files_and_folders.append(nodeobj)
                return
            # anything below depth of 1 needs recursion
            print(node.name, node.path, path)
            while current.directory_id != node.pid and path:
                folder = current.find_folder(path.pop(0))
                print('>>>',folder)
                if not folder:
                    break
                current = folder
                print('current is now', current.name)
            current.files_and_folders.append(nodeobj)
                    
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
    for n in l:
        print(n)
    utils.print_inorder(l)
    utils.print_inorder_indent_tree(l)
    s = System(l)
    print(s.root)
    for n in s.root.files_and_folders:
        print('>>>',n)
    for n in Tree.newgrow(s):
        print(n)

if __name__ == "__main__":
    main()