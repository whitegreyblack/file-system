# __main__.py
import os
import sys
import click
import system.utils as utils
import system.parser as parser
from system.cmd.tree import tree as treecmd
from system.cmd.ls import ls
from system.cmd.cd import cd
from system.system import System


def check_path(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(filepath)


def build_tree(filepath):
    check_path(filepath)
    data = parser.load(filepath)
    l = parser.parse(parser.load(filepath))
    s = System(l)
    out = treecmd(s.root)
    return '\n'.join(out)


def build_path(filepath):
    check_path(filepath)
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
        return f"{f.name.lower():<15}{c:>3}"
    else:
        return f"{f.name.lower():<10}" + str(file_size(f.ref))


def absolute_path(directory):
    if directory.parent_directory == None:
        return f"~/{directory.name.lower()}"
    path = ""
    current = directory
    while current.parent_directory:
        path = current.name + "/" + path
        current = current.parent_directory
    return f"~/{path.lower()}"

def list_directories(directory, ls_long=False):
    return '\n'.join(x.name for x in directory.files_and_folders)

def save_system(nodes):
    filepath = "." + os.path.sep + "saves" + os.path.sep + "save.yaml"
    utils.check_save_directory(filepath)
    data = utils.format_nodes_for_write(nodes)
    utils.write(filepath, data)

def calculate_terminal_size():
    return os.get_terminal_size()

def calculate_max_columns():
    return max(1, calculate_terminal_size().lines)

def file_system(filepath):
    check_path(filepath)

    data = parser.load(filepath)
    l = parser.parse(parser.load(filepath))
    system = System(l)
    current = system.root
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
        # any output is printed here
        if output:
            print(output)
            output = None

        # user input
        try:
            user_input = input(f"{absolute_path(current)}>>> ")
        except (KeyboardInterrupt, EOFError):
            break

        # parse inputs and evaluate (TODO: use lexical tree for quotation inputs)
        cmd, *inputs = user_input.split(' ')

        # detected no input/empty input. Continue waiting for input
        if not cmd or cmd == '':
            continue

        # for all other inputs
        if cmd in ('ls', 'dir'):
            output = ls(current)
        elif cmd in ('col', 'column', 'columns'):
            output = calculate_terminal_size().columns
        elif cmd in ('row', 'rows'):
            output = calculate_terminal_size().lines
        elif cmd in ('maxcol'):
            output = calculate_max_columns()
        elif cmd in ('?', 'help'):
            output = help_string
        # elif cmd == 'save':
        #     save_system(l)
        #     output = save_string
        elif cmd == 'tree':
            output = "\n".join(tree(current))
        elif cmd == 'exit':
            break
        elif cmd == 'cat':
            output = cat()
        # elif cmd == 'cat':
        #     i, *inputs = inputs
        #     if i in set(x.lower() for x in dirnames):
        #         for n in dirnodes:
        #             if i.lower() == n.name.lower():
        #                 if n.cid != '$':
        #                     folder = True
        #                 node = n
        #                 break
        #         if not folder:
        #             output = read_file_contents()
        #         else:
        #             output = error_cat_not_valid.format(n.name, n.name)
        # elif cmd == 'cd':
        #     i, *inputs = inputs
        #     if i == '~':
        #         oldindex, dirindex = dirindex, 0
        #     # going up system level
        #     elif i == '..' and dirindex > 0:
        #         # in an empty folder, no references in directory node list
        #         print(oldindex, dirindex, '<=', dirindex, parnode.gid)
        #         oldindex, dirindex = dirindex, oldindex
        #     # going down system level
        #     elif i.lower() in set(x.lower() for x in dirnames):
        #         node = None
        #         folder = False
        #         # find exact file/directory to move into
        #         for n in dirnodes:
        #             if i.lower() == n.name.lower():
        #                 if n.cid != '$':
        #                     folder = True
        #                 node = n
        #                 break
        #         if folder:
        #             print(oldindex, dirindex, '<=', dirindex, node.cid)
        #             oldindex, dirindex = dirindex, node.cid
        #         else:
        #             output = error_dir_not_valid.format(node.name)
        #     else:
        #         output = error_dir_not_found
        # elif cmd == 'pwd':
        #     output = build_absolute_path(l, dirindex)
        else:
            output = error_cmd_not_valid


@click.command()
@click.option('tree', '--tree', multiple=True, type=click.Path())
@click.option('path', '--path')
def main(tree, path):
    if not tree and not path:
        print("""py -m system [--tree|--path]=[PATH]""")
    elif path:
        file_system(path)
    else:
        for f in tree:
            t = build_tree(f)
            print(t)


if __name__ == '__main__':
    main()
