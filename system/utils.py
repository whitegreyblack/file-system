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
    print('n g c')
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

def print_inorder_indent_tree(t, indent=0):
    *ns, n = elements_indented(t, indent)
    while n:
        n, i = n
        print(f"{' ' * (i * 4)}{n.name}")
        if n.cid:
            for e in elements(t, n.cid):
                ns.append((e, i+1))
        n = None
        if ns:
            n = ns.pop()

def print_inorder_full_path(t, path="", include_dir=False):
    *ns, n = elements_full_path(t)
    while n:
        n, p = n
        if not n.cid:
            print(p+n.name)
        else:
            if include_dir:
                print(p+n.name)
            for e in elements(t, n.cid):
                ns.append((e, p+n.name))            
        n = None
        if ns:
            n = ns.pop()