# utils.py
"""
Holds common functions used throughout the systems package.
"""

import os
import random
from collections import namedtuple


class Node(object):
    def __init__(self, nid, gid, pid, cid, name):
        self.nid = nid
        self.gid = gid
        self.pid = pid
        self.cid = cid
        self.name = name


node = namedtuple("Node", "nid gid pid cid name")
dirsort = lambda x: (x.cid is None, x.name)
dirsortid = lambda x: x.nid
dirfilter = lambda l, i: list(filter(lambda x: x.gid == i, l))
findnode = lambda l, i: list(filter(lambda x: x.nid == i, l))

random_folder_name = lambda: chr(65 + random.randint(0, 25))
random_file_name = lambda: chr(97 + random.randint(0, 25))


def dirsum(nodelist, groupid):
    c = dirfilter(nodelist, groupid)
    count = len(c)
    for n in c:
        count += dirsum(nodelist, n.cid)
    return count


def els_repr(ns):
    return [el_repr(n) for n in ns]


def el_repr(n):
    nid = f"{n.nid:>2}"
    gid = f"{n.gid:>2}"
    pid = f"{n.pid if n.cid else '$':>2}"
    cid = f"{n.cid if n.cid else '$':>2}"
    return f"{nid}  {gid}  {pid}  {cid}  {n.name}"


def elements(t, i=0, sort=dirsort):
    return sorted(dirfilter(t, i), key=dirsort, reverse=True)


def elements_indented(t, i=0, tab=0):
    return [(e, tab) for e in elements(t, i)]


def elements_full_path(t, i=0, path=""):
    return [(e, path) for e in elements(t, i)]


def check_save_directory(filepath):
    pardir = os.path.dirname(filepath)
    if not os.path.exists(pardir):
        os.mkdir(pardir)


def write(filepath, data):
    with open(filepath, "w+") as f:
        f.writelines(data)


def format_nodes_for_write(nodes):
    return print_inorder_indent_tree(nodes, 1)


class Style:
    Default, Tree, Path = range(3)


def print_inorder(t, sort=dirsort):
    *ns, n = elements(t, 0)
    nodes = ["NID GID PID CID Name"]
    while n:
        nodes.append(el_repr(n))
        if n.cid != '$':
            for e in elements(t, i=n.cid, sort=dirsort):
                ns.append(e)
        n = None
        if ns:
            n = ns.pop()
        else:
            break
    print('\n'.join(nodes))
    return '\n'.join(nodes)


def print_inorder_indent_tree(t, level=0, indent_spacing=4):
    *ns, n = elements_indented(t, level)
    nodes = ["NID GID PID CID Name"]
    while n:
        n, indent_level = n
        indent = ' ' * (indent_level * indent_spacing)
        ref = '' if n.ref == '$' else f' => {n.ref}'
        nodes.append(f"{indent}{n.name}{ref}")
        if n.cid:
            child_nodes = elements(t, n.cid)
            for e in child_nodes:
                ns.append((e, indent_level+1))
        n = None
        if ns:
            n = ns.pop()
    print('\n'.join(nodes))
    return '\n'.join(nodes)


def print_inorder_full_path(t, path="~/", include_ref=False):
    *ns, n = elements_full_path(t, path=path)
    nodes = ["NID GID PID CID Name"]
    while n:
        n, p = n
        if not n.cid:
            nodes.append(p+n.name)
        else:
            if not include_ref or n.ref == '$':
                ref = '/'
            else:
                ref = f' => {n.ref}'
            nodes.append(f"{p}{n.name.lower()}{ref}")
            for e in elements(t, n.cid):
                ns.append((e, p + n.name.lower() + "/"))
        n = None
        if ns:
            n = ns.pop()
    print('\n'.join(nodes))
    return '\n'.join(nodes)