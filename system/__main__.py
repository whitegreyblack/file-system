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


def convert_to_specific_os(ref):
    return ref.replace('/', os.path.sep)


def file_size(ref):
    pwd = os.path.abspath(convert_to_specific_os(ref))
    print(pwd)
    size = os.path.getsize(pwd)
    return f"{f'{size} B':>6}"


def format_file_or_folder(f, c):
    if f.cid != '$':
        return f"{f.name.lower():<15}{c:<3}"
    else:
        return f"{f.name.lower():<10}" + str(file_size(f.ref))


def build_absolute_path(l, nid):
    path = ""
    n, *_ = utils.findnode(l, nid)
    if not n:
        raise Exception(f"Could not find node with nid {n.nid}")
    path = f"{n.name}/"
    while n.pid != '$':
        n, *_ = utils.findnode(l, n.pid)
        if n:
            path = f"{n.name}/" + path
    return "~/" + path.lower()


def list_directories(nodelist, dirindex, sorteddir):
    print_list = []
    # print_list.append(f"{'[~/root/]:':<30}#")
    if dirindex > 0:
        print_list.append('..')
    for n in sorteddir:
        c = utils.dirsum(nodelist, n.cid)
        print_list.append(format_file_or_folder(n, c))
    print('\n'.join(print_list))


def save_system(nodes):
    filepath = "." + os.path.sep + "saves" + os.path.sep + "save.yaml"
    utils.check_save_directory(filepath)
    data = utils.format_nodes_for_write(nodes)
    utils.write(filepath, data)


def file_system():
    filepath = "." + os.path.sep + "data" + os.path.sep + "structure.yaml"
    if not os.path.exists(filepath):
        raise FileNotFoundError(filepath)

    data = parser.load(filepath)
    l = parser.parse(parser.load(filepath))

    dirsize = 0
    oldindex = 0
    dirindex = 0

    output = None

    help_string = """
ls/dir : outputs file and folder info in directory
save   : exports current system to yaml format
cat    : outputs selected file contents (TODO: write input to file using '>')
cd     : changes current directory to input directory
exit   : exit program
pwd    : output absolute path
"""[1:]

    save_string = "... System saved to file"
    error_cmd_not_valid = "... Invalid command. Please try again."
    error_dir_not_valid = "... Cannot change directory into '{}'"
    error_dir_not_found = "... Folder or file name not found"
    error_cat_not_valid = "... Could not read '{}'. '{}' is a directory."

    while 1:
        dirnodes = utils.dirfilter(l, dirindex)
        parnode, *_ = utils.findnode(l, dirnodes[0].nid)
        dirnames = list(map(lambda x: x.name.replace('/', ''), dirnodes))
        sorteddir = sorted(dirnodes, key=utils.dirsort)

        # any output is printed here
        if output:
            print(output)
            output = None

        # user input
        try:
            user_input = input(f">>> ")
        except (KeyboardInterrupt, EOFError):
            break

        # parse inputs and evaluate (TODO: use lexical tree for quotation inputs)
        cmd, *inputs = user_input.split(' ')

        # detected no input/empty input. Continue waiting for input
        if not cmd or cmd == '':
            continue

        # for all other inputs
        if cmd in ('ls', 'dir'):
            output = list_directories(l, dirindex, sorteddir)
        elif cmd in ('?', 'help'):
            output = help_string
        elif cmd == 'save':
            save_system(l)
            output = save_string
        elif cmd == 'exit':
            break
        elif cmd == 'cat':
            i, *inputs = inputs
            if i in set(x.lower() for x in dirnames):
                for n in dirnodes:
                    if i.lower() == n.name.lower():
                        if n.cid != '$':
                            folder = True
                        node = n
                        break
                if not folder:
                    output = read_file_contents()
                else:
                    output = error_cat_not_valid.format(n.name, n.name)
        elif cmd == 'cd':
            i, *inputs = inputs
            if i == '~':
                oldindex, dirindex = dirindex, 0
            # going up system level
            elif i == '..' and dirindex > 0:
                # in an empty folder, no references in directory node list
                oldindex, dirindex = dirindex, parnode.gid
            # going down system level
            elif i.lower() in set(x.lower() for x in dirnames):
                node = None
                folder = False

                # find exact file/directory to move into
                for n in dirnodes:
                    if i.lower() == n.name.lower():
                        if n.cid != '$':
                            folder = True
                        node = n
                        break
                if folder:
                    oldindex, dirindex = dirindex, node.cid
                else:
                    output = error_dir_not_valid.format(node.name)
            else:
                output = error_dir_not_found
        elif cmd == 'pwd':
            output = build_absolute_path(l, dirindex)
        else:
            output = error_cmd_not_valid

if __name__ == '__main__':
    main()