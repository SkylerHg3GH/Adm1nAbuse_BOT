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

MAX_ABS_VALUE = 10**100
MAX_POWER = 1000
MAX_SHIFT = 4096
MAX_EXPR_LEN = 200


def safe_eval(expr: str, vars: dict = None):
    if vars is None:
        vars = {}

    if len(expr) > MAX_EXPR_LEN:
        raise ValueError("Expression too long")

    env = {**_CONSTS, **vars}

    expr = expr.replace("^", "**")
    node = ast.parse(expr, mode="eval")

    def check_num(num):
        if isinstance(num, int) and abs(num) > MAX_ABS_VALUE:
            raise ValueError("Number too large")
        return num

    def _eval(cur):
        if isinstance(cur, ast.Expression):
            return _eval(cur.body)

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

            left = _eval(cur.left)
            right = _eval(cur.right)

            # prevent massive powers
            if op_type is ast.Pow:
                if abs(right) > MAX_POWER:
                    raise ValueError("Exponent too large")

            # prevent RAM killer bitshifts
            elif op_type in (ast.LShift, ast.RShift):
                if abs(right) > MAX_SHIFT:
                    raise ValueError("Shift too large")

            result = _OPS[op_type](left, right)

            return check_num(result)

        elif isinstance(cur, ast.UnaryOp):
            op_type = type(cur.op)

            if op_type not in _OPS:
                raise ValueError(f"Unary operator {op_type} not allowed")

            result = _OPS[op_type](_eval(cur.operand))

            return check_num(result)

        raise ValueError(f"Unsupported expression: {type(cur)}")

    return _eval(node)


def main(ctx: Context):
    try:
        expr = " ".join(ctx.args)
        result = safe_eval(expr)

        botlib.followup(ctx.user, f"Answer: '{result}'")

    except Exception:
        botlib.followup(
            ctx.user,
            botlib.cfg["messages"]["invalidExpressionMessage"]
        )