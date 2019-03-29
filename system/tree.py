# tree.py
"""
Takes in a list of file nodes and creates a tree.
"""
import click
import system.utils as utils
import system.parser as parser
from system.system import File, Folder, System
from collections import namedtuple
from datetime import datetime
import os

class Branch(object):
    Edge = "├──"
    Line = "│  "
    Corner = "└──"
    Blank = "   "
    Empty = ""
    
def tree(startnode:object)->str:
    """
    Using the start node and keeping track of depth and last item in directory,
    iterate the system tree structure to generate a list of formatted strings.
    """
    # keep count of all files and folders
    files, folders = 0, 0
    # start node, element count, depth, size of directory, branch prefix
    stack = [(startnode, 0, 0, 1, Branch.Empty)]
    while stack:
        (f, i, d, s, p), *stack = stack
        isfolder = isinstance(f, Folder)
        deep = d > 0
        last = i == s-1
        if isfolder:
            folders += 1
            # add children files/folders to stack
            size = len(f.files_and_folders)
            if size > 0:
                prefix = ""
                if deep:
                    prefix = p + (Branch.Blank if last else Branch.Line)
                nodes = [
                    (f, i, d+1, size, prefix)
                        for i, f, in enumerate(f.files_and_folders)
                ]
                stack = nodes + stack     
            # folder specific formatting
            nid = f"{f.folder_id:2}"
            cid = f"{f.child_directory_id:2}"
            ref = ""
        else:
            files += 1
            # file specific formatting
            nid = f"{f.file_id:2}"
            cid = f"{'$':>2}"
            ref = f" => {f.reference}"
        pid = f"{f.parent_directory_id:>2}"
        # non-specific formatting
        branch = ""
        if deep:
            branch = Branch.Corner if last else Branch.Edge
        # send back the formatted string
        yield f"{nid} {pid} {cid} {p}{branch}{f.name}{ref}"
        if not stack:
            break
    yield f"Directories: {folders}, Files: {files}"

@click.command()
@click.argument('filepath', type=click.Path(exists=True))
def main(filepath:str):
    data = parser.load(filepath)
    nodes = parser.parse(data)
    system = System(nodes)
    for f in tree(system.root):
        print(f)

    for f in tree(System(nodes=parser.parse(parser.load(filepath))).root):
        print(f)

if __name__ == "__main__":
    main()