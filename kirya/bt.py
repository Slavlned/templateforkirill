# built-ins for VRC

def _format(fmt, *args): return fmt % args

def _add(a, b): return a + b

def _le(a, b): return a <= b

def _eq(a, b): return a == b

def _not(a): return not a

def _range(a, b): return range(a, b)

def _print(*a, **kw): print(*a, **kw)

def _input(*a, **kw): return input(*a, **kw)
