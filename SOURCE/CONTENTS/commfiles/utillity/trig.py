from bottype import Context
import botlib
import ast
import operator
import math

_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.LShift: operator.lshift,
    ast.RShift: operator.rshift,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

_CONSTS = {
    "pi": math.pi,
    "e": math.e,
}

_FUNCS = {
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "sinh": math.sinh,
    "cosh": math.cosh,
    "tanh": math.tanh,
    "asin": math.asin,
    "acos": math.acos,
    "atan": math.atan,
    "asinh": math.asinh,
    "acosh": math.acosh,
    "atanh": math.atanh,
    "sqrt": math.sqrt,
    "log": math.log,
    "log10": math.log10,
    "degrees": math.degrees,
    "radians": math.radians,
    "cbrt": math.cbrt,
    "root": lambda num, root: num ** (1 / root),
}

MAX_EXPR_LEN = 200
MAX_POWER = 1000
MAX_SHIFT = 4096
MAX_ABS_INT = 10**100
MAX_AST_DEPTH = 32


def safe_eval(expr: str, vars: dict = None):
    if vars is None:
        vars = {}

    if len(expr) > MAX_EXPR_LEN:
        raise ValueError("Expression too long")

    env = {**_CONSTS, **_FUNCS, **vars}

    expr = expr.replace("^", "**")
    node = ast.parse(expr, mode="eval")

    def check_num(num):
        if isinstance(num, int):
            if abs(num) > MAX_ABS_INT:
                raise ValueError("Integer too large")

        if isinstance(num, float):
            if not math.isfinite(num):
                raise ValueError("Invalid float")

        return num

    def _eval(cur, depth=0):
        if depth > MAX_AST_DEPTH:
            raise ValueError("Expression too deep")

        if isinstance(cur, ast.Expression):
            return _eval(cur.body, depth + 1)

        elif isinstance(cur, ast.Constant):
            if isinstance(cur.value, (int, float)):
                return check_num(cur.value)

            raise ValueError("Invalid constant")

        elif isinstance(cur, ast.Name):
            if cur.id in env:
                return env[cur.id]

            raise ValueError(f"Unknown variable: {cur.id}")

        elif isinstance(cur, ast.BinOp):
            op_type = type(cur.op)

            if op_type not in _OPS:
                raise ValueError(f"Operator {op_type} not allowed")

            left = _eval(cur.left, depth + 1)
            right = _eval(cur.right, depth + 1)

            if op_type is ast.Pow:
                if abs(right) > MAX_POWER:
                    raise ValueError("Exponent too large")

            elif op_type in (ast.LShift, ast.RShift):
                if abs(right) > MAX_SHIFT:
                    raise ValueError("Shift too large")

            result = _OPS[op_type](left, right)

            return check_num(result)

        elif isinstance(cur, ast.UnaryOp):
            op_type = type(cur.op)

            if op_type not in _OPS:
                raise ValueError(f"Unary operator {op_type} not allowed")

            result = _OPS[op_type](_eval(cur.operand, depth + 1))

            return check_num(result)

        elif isinstance(cur, ast.Call):
            if not isinstance(cur.func, ast.Name):
                raise ValueError("Invalid function call")

            func_name = cur.func.id

            if func_name not in _FUNCS:
                raise ValueError(f"Function '{func_name}' not allowed")

            args = [_eval(arg, depth + 1) for arg in cur.args]

            try:
                result = _FUNCS[func_name](*args)
            except Exception:
                raise ValueError("Math domain error")

            return check_num(result)

        raise ValueError(f"Unsupported expression: {type(cur)}")

    return _eval(node)


def main(ctx: Context):
    try:
        expr = " ".join(ctx.args)

        result = safe_eval(expr)

        botlib.followup(
            ctx.user,
            f"Answer: '{result}'"
        )

    except Exception:
        botlib.followup(
            ctx.user,
            botlib.cfg["messages"]["invalidExpressionMessage"]
        )