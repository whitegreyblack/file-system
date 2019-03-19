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


def format_file_or_folder(f, c):
    if f.name.endswith('/'):
        return f"{f.name.lower():<30}{len(c)}"
    else:
        return f.name.lower()


def list_directories(nodelist, dirindex, sorteddir):
    print_list = []
    # print_list.append(f"{'[~/root/]:':<30}#")
    if dirindex > 0:
        print_list.append('..')
    for n in sorteddir:
        c = utils.dirfilter(nodelist, n.cid)
        print_list.append(format_file_or_folder(n, c))
    print('\n'.join(print_list))


def file_system():
    filepath = "." + os.path.sep + "data" + os.path.sep + "structure.yaml"
    if not os.path.exists(filepath):
        raise FileNotFoundError(filepath)

    data = parser.load(filepath)
    l = parser.parse(parser.load(filepath))
    print(l)

    dirsize = 0
    dirindex = 0
    dir_print = False

    save = False
    save_string = "... System saved to file"

    selected = None
    selected_string = "... Selected File: {}"

    error = False
    error_string = "... Folder or File name not found"

    while 1:
        dirnodes = utils.dirfilter(l, dirindex)
        dirnames = list(map(lambda x: x.name.replace('/', ''), dirnodes))
        sorteddir = sorted(dirnodes, key=utils.dirsort)

        # print directory if last action was ls or dir
        if dir_print:
            list_directories(l, dirindex, sorteddir)
            dir_print = False

        # print error from last action
        if error:
            print(error_string)
            error = False

        # print selected file from last action
        if selected:
            selectedpath = 'data' + os.path.sep + selected.name
            print(parser.read(selectedpath))
            selected = None

        # save system and print confirmation
        if save:
            print(save_string)
            save = False

        # user input
        try:
            user_input = input(">>> ")
        except (KeyboardInterrupt, EOFError):
            break

        # parse inputs and evaluate
        cmd, *inputs = user_input.split(' ')
        if not cmd or cmd == '':
            continue
        if cmd == 'ls' or cmd == 'dir':
            dir_print = True
        elif cmd == 'save':
            save = True
        elif cmd == 'exit':
            break
        elif cmd == 'cd':
            i, *inputs = inputs
            # going up system level
            if i == '..' and dirindex > -1:
                print('Dirindex: ', dirindex)
                parentnode = next(filter(lambda x: x.nid == dirnodes[0].pid, l))
                print('Parentnode', parentnode.gid)
                dirindex = parentnode.gid
            # going down system level
            elif i in dirnames:
                node = None
                folder = False

                # find exact file/directory to move into
                for i, n in enumerate(dirnodes):
                    if n.name.replace('/', '') == user_input:
                        if n.name.endswith('/'):
                            folder = True
                        node = n
                        break
                if folder:
                    dirindex = -2
                    if node.cid:
                        dirindex = node.cid
                else:
                    selected = node            
            else:
                error = True
        else:
            error = True

if __name__ == '__main__':
    main()