# __main__.py
import os
import sys
import system.utils as utils
import system.parser as parser
import system.hashsystem as hashsys
import system.listsystem as listsys
import system.hashlistsystem as hlsys

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
        print('..')
        for n in sorteddir:
            print(n.name)
        dir_print = False
    if error:
        print(error_string)
        error = False
    if selected:
        print(selected_string.format(selected.name))
        selected = None

    try:
        file_or_folder = input(">>> ")
    except (KeyboardInterrupt, EOFError):
        break

    if file_or_folder not in dirnames:
        if file_or_folder == '..' and dirindex != 0:
            parentnode = next(filter(lambda x: x.nid == dirnodes[0].pid, l))
            dirindex = parentnode.gid
        elif file_or_folder == 'ls' or file_or_folder == 'dir':
            dir_print = True
        else:
            error = True
    else:
        node = None
        folder = False
        for i, n in enumerate(dirnodes):
            if n.name.endswith('/'):
                folder = True
            if n.name.replace('/', '') == file_or_folder:
                node = n
                break
        if folder:
            dirindex = -1
            if node.cid:
                dirindex = node.cid
        else:
            selected = node