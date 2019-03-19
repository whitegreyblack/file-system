# test parser functions
import system.parser as p
import os

filepath = "data" + os.path.sep + "structure.yaml"

def test_read():
    assert type(p.read(filepath)) is str

def test_load():
    assert type(p.load(filepath)) is dict

def test_deserialize():
    d = {
        'Documents': [{
            'file': 'data/file',
            'Folder': [{
                'text': 'data/text'
            }]
        }],
        'Music': []
    }
    print(d)

if __name__ == "__main__":
    test_deserialize()