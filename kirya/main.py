from parglare import Grammar, Parser, ParseError
import sys


def lpp(lst, ind = 0):
    print(" " * ind + "[")
    for i in lst:
        if isinstance(i, list):
            lpp(i, ind + 1)
        else:
            print(" " * ind + str(i))
    print(" " * ind + "]")



def action(node, children):
    if not isinstance(children, list):
        return [children]
    if children[0] == '`':
        children = children[1:-1]
        if len(children) > 1:
            if not children[1]:
                return children[:1]
        return children[0]
    return children[0]

grammar = Grammar.from_file('vrc.pgl')
parser = Parser(grammar, actions={
    "list": action,
    "string": lambda _, x: ["string", x],
    "integer": lambda _, x: ["int", x],
    "float": lambda _, x: ["float", x]
})

def compile_list(children):
    #print("Processing:")
    if isinstance(children, str):
        children = [children]
    #pp(children, indent = 2)
    name = children[0]
    args = children[1:]
    if name == "root":
        src = "\n".join(compile_list(arg) for arg in args)
    
    elif name == "fn":
        #print(args[2])
        name = "_" + args[0]
        body = args[2:]
        args = args[1]
        src = f"def {name}({', '.join(args)}):\n    "
        src += "\n    ".join(compile_list(arg).replace("\n", "\n    ") for arg in body)
        src += "\n"
    
    elif name == "if":
        cond = args[0]
        body = args[1:]
        src = f"if {compile_list(cond).strip()}:\n    "
        src += "\n    ".join(compile_list(arg).replace("\n", "\n    ") for arg in body)
        src += "\n"
    
    elif name == "for":
        iterator = args[0]
        iterable = args[1]
        body = args[2:]
        src = f"for {iterator} in {compile_list(iterable).strip()}:\n    "
        src += "\n    ".join(compile_list(arg).replace("\n", "\n    ") for arg in body)
        src += "\n"
    
    elif name == "return":
        if len(args) == 0:
            return "return\n"
        else:
            return "return " + compile_list(args[0]).strip() + "\n"
    
    elif name == "set":
        iterator = compile_list(args[0]).strip()
        value = compile_list(args[1]).strip()
        src = f"{iterator} = {value}\n"
    
    elif name == "REM":
        src = f"# {' '.join(args)}\n"
    
    elif name in ("int", "float", "string"):
        return args[0]
    elif name[0] == "$":
        return f"{name[1:]}"
    else:
        src = f"_{name}({', '.join(compile_list(arg).strip() for arg in args)})\n"
    
    #print("Result:")
    #print(src)
    return src

try:
    inf = sys.argv[0]
    code = compile_list(["root", *parser.parse_file(inf)])
    with open("bt.py", "rt") as f:
        code = f.read() + "\n\n" + code
    pycode = compile(code, inf, 'exec', dont_inherit=True, optimize=2)
    exec(pycode)
except ParseError as e:
    print(e)
    sys.exit(1)
except Exception as e:
    print(e)
    sys.exit(1)
