# interpreter.py

"""
parses text or file input into tree commands
"""

# TODO: ultimate objective is to get tree.py to accept inputs:
#           insert random 100
#           insert 0..100 || insert 0...100?
space = ' ' 
numeric = set('1234567890.')
alpha = set('abcdefghijklmnopqrstuvwxyz')

class TOKEN_TYPES:
    WORD = 'WORD'                # action, insert
    FLOAT = 'FLOAT'              # 1.0, 1.01, .01
    INTEGER = 'INTEGER'          # 1, 12, 123
    RANGE_IN = 'RANGE_INCLUSIVE' # '..'
    RANGE_EX = 'RANGE_EXCLUSIVE' # '...'

class Operators(object):
    OP_PLUS = '+'
    OP_MINUS = '-'
    OP_RANGE_IN = '..'
    OP_RANGE_EX = '...'

class Interpreter(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None
        self.current_char = self.text[self.pos]

    def next_token(self):
        while self.current_char is not None:
            char_is_valid = True
            if self.current_char is space:
                char_is_space = True
                while char_is_valid and char_is_space:
                    self.pos += 1
                    if self.pos <= len(self.text) - 1:
                        self.current_char = self.text[self.pos]
                    else:
                        self.current_char = None
                    char_is_valid = self.current_char is not None
                    char_is_space = self.current_char is space
                continue
            if self.current_char in alpha:
                beg = self.pos
                char_is_alpha = True
                while char_is_valid and char_is_alpha:
                    self.pos += 1
                    if self.pos <= len(self.text) - 1:
                        self.current_char = self.text[self.pos]
                    else:
                        self.current_char = None
                    char_is_valid = self.current_char is not None
                    char_is_alpha = self.current_char in alpha
                if char_is_valid and not char_is_alpha:
                    # we got a [^a-z] character -- invalidate
                    print("Syntax error. Action has numeric characters. Not allowed")
                    return None
                return self.text[beg:self.pos+1]
        return 'EOF'

if __name__ == "__main__":
    i = Interpreter(input('>>> '))
    print(i.next_token())

