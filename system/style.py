# from pygments.style import Style
# from pygments.token import Keyword, Comment, String, Error, Number, Operator, Generic

# class YourStyle(Style):
#     default_style = ""
#     styles = {
#         Comment:                'italic #888',
#         Keyword:                'bold #005',
#         Name:                   '#f00',
#         Name.Function:          '#0f0',
#         Name.Class:             'bold #0f0',
#         String:                 'bg:#eee #111'
#     }

from pygments import highlight
from pygments.style import Style
from pygments.token import Token
from pygments.lexers import Python3Lexer
from pygments.formatters import TerminalFormatter, Terminal256Formatter
# class MyStyle(Style):
#         styles = {
#             Token.String:     'bg:#0f0 #00f',
#         }
code = 'print("Hello World")'
result = highlight(code, Python3Lexer(), TerminalFormatter(style=Style))
print(result)
result = highlight(code, Python3Lexer(), Terminal256Formatter(style=Style))
print(result)

from colorama import Fore, Back, Style
print(Fore.RED + 'some red text')
print(Back.GREEN + 'and with a green background')
print(Style.DIM + 'and in dim text')
print(Style.RESET_ALL)
print('back to normal now')