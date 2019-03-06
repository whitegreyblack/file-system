# __main__.py
import os
import system.utils as utils
import system.parser as parser
import system.hashsystem as hashsys
import system.listsystem as listsys
import system.hashlistsystem as hlsys

filepath = input("Enter in a datafile (Press <ENTER> to use default file): ")
if not filepath:
    filepath = "." + os.path.sep + "data" + os.path.sep + "structure.yaml"
print(filepath)
if not os.path.exists(filepath):
    raise FileNotFoundError(filepath)
print(parser.read(filepath))
data = parser.load(filepath)
print(data)
l = parser.parse(data)
