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

class Tree (object):
    Edge = "├──"
    Line = "│  "
    Corner = "└──"
    Blank = "   "
    Empty = ""
    
    @staticmethod
    def grow(startnode):
        stack = [(startnode, 0, 0, 1, Tree.Empty)]
        while stack:
            (f, i, d, s, p), *stack = stack
            isfolder = isinstance(f, Folder)
            if isfolder:
                nid = f"{f.folder_id:2}"
                cid = f"{f.child_directory_id:2}"
            else:
                nid = f"{f.file_id:2}"
                cid = f"{'$':>2}"
            pid = f"{f.parent_directory_id:>2}"
            link = ""
            if d > 0:
                link = Tree.Corner if i == s-1 else Tree.Edge
            noderow = f"{nid} {pid} {cid} {p}{link}{f.name}"
            if not isfolder:
                noderow += f" => {f.reference}"
            yield noderow
            if isfolder:
                size = len(f.files_and_folders)
                if size == 0:
                    continue
                prefix = ""
                if d > 0:
                    prefix = p + Tree.Line
                    if i == s-1:
                        prefix = p + Tree.Blank
                nodes = [
                    (f, i, d+1, size, prefix)
                        for i, f, in enumerate(f.files_and_folders)
                ]
                stack = nodes + stack            
            if not stack:
                break

@click.command()
@click.argument('filepath', type=click.Path(exists=True))
def main(filepath):
    data = parser.load(filepath)
    nodes = parser.parse(data)
    system = System(nodes)
    for f in Tree.grow(system.root):
        print(f)

if __name__ == "__main__":
    main()