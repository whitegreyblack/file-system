# utils.py
"""
Holds common functions used throughout the systems package.
"""
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
dirfilter = lambda l, i: list(filter(lambda x: x.gid == i, l))

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
    return f"{n.nid} {n.gid} {n.cid if n.cid else '|'} {n.name}"

def elements(t, i=0):
    elms = sorted(dirfilter(t, i), key=dirsort, reverse=True)
    return elms

def elements_indented(t, i=0, tab=0):
    return [(e, tab) for e in elements(t, i)]

def elements_full_path(t, i=0, path=""):
    return [(e, path) for e in elements(t, i)]

def print_inorder(t):
    *ns, n = elements(t, 0)
    while n:
        print(el_repr(n))
        if n.cid:
            for e in elements(t, n.cid):
                ns.append(e)
        n = None
        if ns:
            n = ns.pop()
        else:
            break

def print_inorder_indent_tree(t, level=0):
    *ns, n = elements_indented(t, level)
    nodes = []
    while n:
        n, indent_level = n
        nodes.append(f"{' ' * (indent_level * 4)}{n.name}")
        if n.cid:
            child_nodes = elements(t, n.cid)
            for e in child_nodes:
                ns.append((e, indent_level+1))
        n = None
        if ns:
            n = ns.pop()
    print('\n'.join(nodes))

def print_inorder_full_path(t, path="~/", include_dir=True):
    *ns, n = elements_full_path(t, path=path)
    nodes = []
    while n:
        n, p = n
        if not n.cid:
            nodes.append(p+n.name)
        else:
            nodes.append(f"{p if include_dir else ''}{n.name.lower()}")
            for e in elements(t, n.cid):
                ns.append((e, p + n.name.lower() + "/"))
        n = None
        if ns:
            n = ns.pop()
    print('\n'.join(nodes))