# utils.py
import ast
import operator as op
from datetime import datetime

# supported operators
ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.USub: op.neg,
}

def _eval(node):
    if isinstance(node, ast.Constant):  # Python 3.8+: ast.Num is merged
        return node.value
    if isinstance(node, ast.Num):
        return node.n
    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        oper = ALLOWED_OPERATORS[type(node.op)]
        return oper(left, right)
    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        oper = ALLOWED_OPERATORS[type(node.op)]
        return oper(operand)
    raise TypeError(f"Unsupported expression: {node}")

def safe_eval(expr: str):
    """
    Safely evaluate a numeric expression with +,-,*,/,%,**, parentheses.
    """
    expr = expr.replace("^", "**")
    parsed = ast.parse(expr, mode="eval")
    return _eval(parsed.body)

def format_time(dt: datetime):
    return dt.strftime("%I:%M %p")
