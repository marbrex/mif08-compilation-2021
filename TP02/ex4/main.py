from antlr4 import InputStream
from antlr4 import CommonTokenStream

# include to use the generated lexer and parser
from Exo4Lexer import Exo4Lexer
from Exo4Parser import Exo4Parser

import sys


def main():
    input_stream = InputStream(sys.stdin.read())
    lexer = Exo4Lexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = Exo4Parser(stream)
    parser.r()
    print("Finished")


# warns pb if py file is included in others
if __name__ == '__main__':
    main()
