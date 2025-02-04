import enum


# Тип токена #
class TokenType(enum.Enum):
    NUMBER = 0
    OPERATOR = 1
    ID = 2
    BRACKET = 3
    ASSIGN = 4
    COMMA = 5

class Token:
    def __init__(self, type: TokenType, value: str):
        self.type = type
        self.value = value

class Lexer:
    def __init__(self, code: str):
        self.cur = 0
        self.code = code
        self.line = 0
        self.tokens: list[Token] = []

    def parse(self) -> list[Token]:
        while self.cur < len(self.code):
            if self.peek(0).isnumeric():
                numb = self.peek(0)
                a = 1
                while self.peek(a).isnumeric():
                    numb += self.peek(a)
                    a += 1
                self.tokens.append(Token(
                    TokenType.NUMBER,
                    numb
                ))
                self.next(a)
                continue
            elif self.peek(0) == "(" or self.peek(0) == ")":
                self.tokens.append(Token(
                    TokenType.BRACKET,
                    self.peek(0)
                ))
                self.next(1)
                continue
            elif self.peek(0) == "+" or self.peek(0) == "-" or self.peek(0) == "*" or self.peek(0) == "/":
                self.tokens.append(Token(
                    TokenType.OPERATOR,
                    self.peek(0)
                ))
                self.next(1)
            elif self.peek(0) == "=":
                self.tokens.append(Token(
                    TokenType.ASSIGN,
                    self.peek(0)
                ))
                self.next(1)
            elif self.peek(0) == ",":
                self.tokens.append(Token(
                    TokenType.COMMA,
                    self.peek(0)
                ))
                self.next(1)
            elif self.peek(0).isalpha():
                id = self.peek(0)
                a = 1
                while self.peek(a).isalpha():
                    id += self.peek(a)
                    a += 1
                self.tokens.append(Token(
                    TokenType.ID,
                    id
                ))
                self.next(a)
                continue
            else:
                self.next(1)
        return self.tokens

    def peek(self, i: int) -> str:
        return self.code[self.cur + i]

    def next(self, i: int) -> None:
        self.cur += i
