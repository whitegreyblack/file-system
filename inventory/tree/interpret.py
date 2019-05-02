# interpret.py

"""
@parameter = text: str NOT NONE

parses text or file input into typed tokens.

Analysis:
    This function allows more control and versatility over input than splitting
    user input by spaces. There could be an indeterminate number of whitespace
    or even invalid characters which can be included with user input which
    can be excluded using this function.
    If an input is valid and no errors are found with any tokens, then the 
    function returns with a list of typed tokens containing split text.
    If any errors are found then the error is logged and function returns early
    with an empty token list.
"""

from dataclasses import dataclass as struct
from repl import user_input

@struct
class Token:
    text: str
    type: str

# TODO: ultimate objective is to get tree.py to accept input insert random 100
space = ' ' 
numeric = set('1234567890')
alpha = set('abcdefghijklmnopqrstuvwxyz')
NUMBER = "NUMBER"
LETTER = "LETTER"

def is_valid(x):
    return x is not None

def is_number(x):
    return x in numeric

def is_letter(x):
    return x in alpha

def next_char(text, pos) -> (str, None):
    return text[pos] if (pos <= len(text) - 1) else None

def mixed_error(text, pos):
    return f"""
  Syntax error. Found mixed characters in word:
    {text}
    {' ' * pos}^"""[1:]

def invalid_error(text, pos):
    return f"""
  Syntax error. Found invalid characters at:
    {text}
    {' ' * pos}^"""[1:]

def tokenize(text) -> list:
    """
    Parses input and returns valid input as typed tokens
    """
    tokens = []
    if not text:
        return tokens
    beg, pos = 0, 0
    char = text[pos] 
    while char is not None:
        # consume chars until EOL
        char_is_valid = True
        if char is space:
            # consume characters until next non space char
            char_is_space = True
            while char_is_valid and char_is_space:
                pos += 1
                char = next_char(text, pos)
                char_is_valid = is_valid(char)
                char_is_space = char is space
        elif is_letter(char):
            # consume characters until not letter char
            beg = pos
            char_is_alpha = True
            while char_is_valid and char_is_alpha:
                pos += 1
                char = next_char(text, pos)
                char_is_valid = is_valid(char)
                char_is_alpha = is_letter(char)
            if char in numeric:
                print(mixed_error(text, pos))
                return []
            if not char_is_valid or char is space:
                tokens.append(Token(text[beg:pos], LETTER))
        elif is_number(char):
            # consume characters until not number char
            beg = pos
            char_is_number = True
            while char_is_valid and char_is_number:
                pos += 1
                char = next_char(text, pos)
                char_is_valid = is_valid(char)
                char_is_number = is_number(char)
            if char in alpha:
                print(mixed_error(text, pos))
                return []
            if not char_is_valid or char is space:
                tokens.append(Token(text[beg:pos], NUMBER))
        else:
            print(invalid_error(text, pos))
            return []
    return tokens

def interpret(tokens) -> object:
    """
    Reads tokens to create a simple abstract syntax tree
    """
    if not tokens:
        return ""
    while tokens:
        token, *tokens = tokens
        if token.type is LETTER:
            # function call
            ts = tokens
            while tokens:
                t, *tokens = tokens
                if t.type is LETTER:
                    ...
                break
        break
    return NotImplemented

def handle_input(user_input):
    """
    function hook to pass into repl loop
    """
    output = []
    tokens = tokenize(user_input)
    for token in tokens:
        output.append(f"{token.text} {token.type}")
    interpreted = interpret(tokens)
    if interpreted:
        output.append(str(interpreted))
    return output

if __name__ == "__main__":
    user_input(fn=handle_input)

