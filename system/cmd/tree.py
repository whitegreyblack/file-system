# tree.py
"""
Takes in a list of file nodes and creates a tree.
"""
import os
import sys
from collections import namedtuple
from datetime import datetime

import click
from colorama import Back, Fore, Style, init

import system.parser as parser
import system.utils as utils
from system.system import File, Folder, System


class TreeArgs(object):
    Color = 1

class Branch(object):
    Edge = "├──"
    Line = "│  "
    Corner = "└──"
    Blank = "   "
    Empty = ""

def check(flag, value):
    return value & flag == flag

def tree(startnode:object, args=None) -> str:
    """
    Using the start node and keeping track of depth and last item in directory,
    iterate the system tree structure to generate a list of formatted strings.
    """
    # keep count of all files and folders
    files, folders = 0, 0
    # start node, element count, depth, size of directory, branch prefix
    stack = [(startnode, 0, 0, 1, Branch.Empty)]
    while stack:
        # TODO: refactor and use better variables
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
            follow = ""
        else:
            files += 1
            # file specific formatting
            nid = f"{f.file_id:2}"
            cid = f"{'$':>2}"
            follow = " => "
            ref = f"{f.reference}"
        pid = f"{f.parent_directory_id:>2}"
        # non-specific formatting
        branch = ""
        if deep:
            branch = Branch.Corner if last else Branch.Edge
        # send back the formatted string
        # yield f"{nid} {pid} {cid} {p}{branch}{f.name}{ref}"
        output = None
        if args:
            colorized = check(TreeArgs.Color, args)
            if colorized:
                b = branch
                n = f.name
                end = Style.RESET_ALL
                if isfolder:
                    fg = Fore.BLUE
                    output = f"{p}{b}{fg}{n}{end}"
                else:
                    fg = Fore.GREEN
                    output = f"{p}{b}{n}{follow}{fg}{ref}{end}"
        if not output:
            output =  f"{p}{branch}{f.name}{follow}{ref}"
        yield output        
        if not stack:
            break
    yield f"Directories: {folders}, Files: {files}"

@click.command()
@click.argument('filepath', type=click.Path(exists=True))
@click.option("--color", "color", is_flag=True, default=False)
def main(filepath:str, color:bool):
    data = parser.load(filepath)
    nodes = parser.parse(data)
    system = System(nodes)

    args = 0
    if color:
        args |= TreeArgs.Color

    for f in tree(system.root, args=args):
        print(f)
                
if __name__ == "__main__":
    from colorama import init
    init()
    main()
