"""
system.py: Data representation of a filesystem

End Goal: (using either B+ tree or Array based directory)
    After structuring, should become:
    Directory
    |__ Documents/
    | |__ Projects/
    | |__ Games/
    | |__ History/
    |__ Music/
    |__ Pictures/
    | |__ Family Pictures/
    | |__ random_photo.png
    |__ out_of_place.png
    |__ verylongfilename_..._.png
"""
data2 = [
    ("Documents", [
        ("Projects", [
            # "File1.png",
            # "File2.txt",
        ]),
        ("Games", []),
    ]),
    ("Music", []),
    ("Pictures", []),
    ("Desktop", [
        ("Stuff", [])
    ]),
    "Out_Of_Place_File.txt",
]

data = [
    ("Documents", [
        ("Projects", []),
        ("Games", []),
        ("History 101", []),
    ]),
    ("Music", []),
    ("Pictures", [
        ("Family Pictures", [
            "Photo_1.png",
            "Photo_2.png"
        ]),
        "Random_Photo.png"
    ]),
    "Out_Of_Place_File.txt",
    # this makes sure we stay within a specific name len
    "VeryLongFileName" + "_" * 60 + ".txt"
]


class Directory(object):
    def __init__(self, parent=None, sysobjs=None):
        self.parent = parent
        self.folders = []
        self.files = []
        self.children = {}

        for sysobj in sysobjs:
            if isinstance(sysobj, tuple):
                name, children = sysobj
                self.folders.append(SystemObject.Folder(name))
                self.children[name] = Directory(self, children)

            if isinstance(sysobj, str):
                self.files.append(SystemObject.File(sysobj))

    def __len__(self):
        return len(self.folders) + len(self.files)

    def __iter__(self):
        return iter(self.folders + self.files)

    def print_tree(self, level=0):
        # fix level spacing
        def get_spacing(level):
            return max(level, 0) * 2

        enum_end = len(self.folders)
        for i, f in enumerate(sorted(str(folder) for folder in self.folders)):
            addr = ""
                # addr = u'\u2502' + u'\u0020' * get_spacing(level) + u'\u2514\u2500'
            if level == 0:
                if enum_end == i+1 and len(self.files) == 0:
                    addr = u'\u2514'
                else:
                    addr = u'\u251C'
                addr += u'\u2500\u0020'
            else:
                if len(self.files) == 0:
                    addr += u'\u0020'
                else:
                    addr += u'\u2502'
                addr += u'\u0020' * get_spacing(level)

                if enum_end == i+1:
                    addr += u'\u2514'
                else:
                    addr += u'\u251C'
                addr += u'\u2500\u0020'

            # print(addr + str(f))
            print(addr + str(f))

            children = self.children.get(f[:-1], None)
            if children:
                children.print_tree(level+1)

        enum_end = len(self.files)
        for i, f in enumerate(self.files):
            # if enum_end == i+1:
            #     addr = u'\u2502' + u'\u0020' * ((level+1) // 2) + u'\u2514\u2500'
            if level == 0:
                if enum_end == i + 1:
                    addr = u'\u2514'
                else:
                    addr = u'\u251C'
                addr += u'\u2500\u0020'
            # else:
            #     addr = u'\u2502' + u'\u0020' * ((level+1) // 2) + u'\u251C\u2500'
            # print(addr+str(f))
            print(addr+str(f))

class SystemObject(object):
    def __init__(self, name:str, isdir:bool=False):
        self.name = name
        self.isdir = isdir

    def __str__(self):
        return self.name + ("/" if self.isdir else "")

    def __repr__(self):
        if isdir:
            return f"Folder({self.name})"
        return f"File({self.name})"
    
    @classmethod
    def Folder(cls, name):
        return SystemObject(name, True)
    
    @classmethod
    def File(cls, name):
        return SystemObject(name)


if __name__ == "__main__":
    import pprint as p

    for i in range(4):
        print(max(i, 0)*2)

    print('2514', '\u2514')
    print('2500', '\u2500')
    print('2502', '\u2502')
    print('251C', '\u251c')
    print('0020', '\u0020')
    print('a' + '\u0020\u0020' + 'b')

    Directory(sysobjs=data2).print_tree()