# __main__.py
import os
import sys
import click
import system.utils as utils
import system.parser as parser
import system.hashsystem as hashsys
import system.listsystem as listsys
import system.hashlistsystem as hlsys

@click.command()
@click.option('tree', '--tree', is_flag=True, default=None)
@click.option('path', '--path', is_flag=True, default=None)
def main(tree, path):
    if not tree and not path:
        file_system()
    elif path:
        build_path()
    else:
        build_tree()

def build_tree():
    filepath = "." + os.path.sep + "data" + os.path.sep + "structure.yaml"
    if not os.path.exists(filepath):
        raise FileNotFoundError(filepath)
    
    data = parser.load(filepath)
    l = parser.parse(parser.load(filepath))
    parser.print_inorder_indent_tree(l)

def build_path():
    filepath = "." + os.path.sep + "data" + os.path.sep + "structure.yaml"
    if not os.path.exists(filepath):
        raise FileNotFoundError(filepath)
    
    data = parser.load(filepath)
    l = parser.parse(parser.load(filepath))
    parser.print_inorder_full_path(l)

def file_system():
    filepath = "." + os.path.sep + "data" + os.path.sep + "structure.yaml"
    if not os.path.exists(filepath):
        raise FileNotFoundError(filepath)

    data = parser.load(filepath)
    l = parser.parse(parser.load(filepath))

    dirsize = 0
    dirindex = 0
    dir_print = False

    selected = None
    selected_string = "... Selected File: {}"

    error = False
    error_string = "... Folder or File name not found"

    while 1:
        dirnodes = utils.dirfilter(l, dirindex)
        dirnames = list(map(lambda x: x.name.replace('/', ''), dirnodes))
        sorteddir = sorted(dirnodes, key=utils.dirsort)
        if dir_print:
            if dirindex > -1:
                print('..')
            for n in sorteddir:
                print(n.name)
            dir_print = False
        if error:
            print(error_string)
            error = False
        if selected:
            selectedpath = 'data' + os.path.sep + selected.name
            print(parser.read(selectedpath))
            selected = None
        try:
            user_input = input(">>> ")
        except (KeyboardInterrupt, EOFError):
            break
        if user_input not in dirnames:
            if user_input == '..' and dirindex > -1:
                parentnode = next(filter(lambda x: x.nid == dirnodes[0].pid, l))
                dirindex = parentnode.gid
            elif user_input == 'ls' or user_input == 'dir':
                dir_print = True
            elif user_input == 'save':
                parser.serialize_list(l)
            elif user_input == 'exit':
                break
            else:
                error = True
        else:
            node = None
            folder = False
            print(dirnodes)
            for i, n in enumerate(dirnodes):
                if n.name.replace('/', '') == user_input:
                    if n.name.endswith('/'):
                        folder = True
                    node = n
                    break
            print(folder)
            if folder:
                dirindex = -2
                if node.cid:
                    dirindex = node.cid
            else:
                selected = node

if __name__ == '__main__':
    main()