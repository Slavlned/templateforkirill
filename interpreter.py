import sys

stack = []

def push():
    stack.append({})

def pop():
    stack.pop()

def get():
    return stack[len(stack)-1]

class PrintFunction:
    def execute(self, args: list) -> any:
        if len(args) < 1:
            print('Invalid Args Amount In Print Function!')
            sys.exit()
        print(args[0].eval())
        return None

class EnterNumFunction:
    def execute(self, args: list) -> any:
        return int(input())

class BlockStatement:
    def __init__(self, statements: list[any]):
        self.statements = statements

    def exec(self):
        push()
        for s in self.statements:
            s.exec()
        pop()

class AssignLocalStatement:
    def __init__(self, name: str, value: any):
        self.name = name
        self.value = value

    def exec(self):
        get()[self.name] = self.value.eval()

class CallLocalStatementExpr:
    def __init__(self, name: str, args: list):
        self.name = name
        self.args = args

    def exec(self):
        functions[self.name].execute(self.args)

    def eval(self) -> any:
        return functions[self.name].execute(self.args)

class GetLocalVarExpr:
    def __init__(self, name: str):
        self.name = name

    def eval(self) -> any:
        return get()[self.name]

class ArithEpxression:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def eval(self) -> any:
        if self.op == "+":
            return self.left.eval() + self.right.eval()
        elif self.op == "-":
            return self.left.eval() - self.right.eval()
        elif self.op == "*":
            return self.left.eval() * self.right.eval()
        elif self.op == "/":
            return self.left.eval() / self.right.eval()
        else:
            print('Invalid Opeartor: ' + self.op)
            sys.exit()

class NumberExpression:
    def __init__(self, value: str):
        self.value = value

    def eval(self) -> any:
        return int(self.value)

functions = {
    "print": PrintFunction(),
    "enternum": EnterNumFunction()
}