import sys

from interpreter import *
from lexer import Token, TokenType


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.cur = 0

    def parse(self) -> any:
        statements = []
        while self.cur < len(self.tokens):
            statements.append(self.statement())
        return BlockStatement(statements)

    def identifier(self) -> any:
        name = self.consume(TokenType.ID).value
        if self.check(TokenType.ASSIGN):
            self.consume(TokenType.ASSIGN)
            return AssignLocalStatement(name, self.expr())
        elif self.check(TokenType.BRACKET) and self.match("("):
            self.consume(TokenType.BRACKET)
            expr = CallLocalStatementExpr(name, self.args())
            self.consume(TokenType.BRACKET)
            return expr
        else:
            return GetLocalVarExpr(name)

    def multiplicative(self) -> any:
        l = self.primary()

        while self.check(TokenType.OPERATOR) and (self.match("*") or self.match("/")):
            operator = self.consume(TokenType.OPERATOR).value
            r = self.primary()
            l = ArithEpxression(l, operator, r)

        return l

    def primary(self) -> any:
        if self.check(TokenType.ID):
            return self.identifier()
        elif self.check(TokenType.NUMBER):
            return NumberExpression(self.consume(TokenType.NUMBER).value)
        elif self.check(TokenType.BRACKET):
            self.consume(TokenType.BRACKET)
            expr = self.expr()
            self.consume(TokenType.BRACKET)
            return expr
        else:
            print(f"""Unexpected Token At (Primary Expr): {self.cur}. Provided: 
            {self.tokenInfo()}""")
            sys.exit()

    def additive(self) -> any:
        l = self.multiplicative()

        while self.check(TokenType.OPERATOR) and (self.match("+") or self.match("-")):
            operator = self.consume(TokenType.OPERATOR).value
            r = self.multiplicative()
            l = ArithEpxression(l, operator, r)

        return l

    def expr(self) -> any:
        expression = self.additive()
        return expression

    def args(self) -> list[any]:
        if self.check(TokenType.BRACKET) and self.match(")"):
            return []

        args_list = [self.expr()]

        while self.check(TokenType.COMMA):
            self.consume(TokenType.COMMA)
            args_list.append(self.expr())

        return args_list

    def statement(self) -> any:
        if self.check(TokenType.ID):
            return self.identifier()
        else:
            print(f"""
            Invalid Token For Statement:
            {self.tokenInfo()}""")
            sys.exit()

    def check(self, expected: TokenType) -> bool:
        if self.cur < len(self.tokens):
            return self.tokens[self.cur].type == expected
        else:
            return False

    def match(self, expected: str) -> bool:
        if self.cur < len(self.tokens):
            return self.tokens[self.cur].value == expected
        else:
            return False

    def consume(self, expected: TokenType) -> Token:
        if not self.check(expected):
            print(f"""Unexpected Token At: {self.cur}. 
            Expected: {expected}. Provided: 
            {self.tokenInfo()}""")
            sys.exit()
        else:
            t = self.tokens[self.cur]
            self.cur += 1
            return t

    def tokenInfo(self):
        i = self.cur
        if self.cur >= len(self.tokens):
            i = self.cur-1
        return f"""{self.tokens[i].type}::
        {self.tokens[i].value}"""