from lexer import Token, Lexer
from parser import Parser

code = """
    a = 2 + 2 * 2
    b = (a + 3) * 2 * enternum()
    print(b)
"""

tokens: list[Token] = Lexer(code).parse()
ast = Parser(tokens).parse()
ast.exec()