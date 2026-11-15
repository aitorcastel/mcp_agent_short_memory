import ast
import operator

SAFE_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

class CalculatorTool:
    def __init__(self):
        self.name = "Calculator"
        self.description = "A tool for performing basic arithmetic calculations."

    def _eval_node(self, node):
        if isinstance(node, ast.Expression):
            return self._eval_node(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in SAFE_OPS:
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            return SAFE_OPS[type(node.op)](left, right)
        if isinstance(node, ast.UnaryOp) and type(node.op) in SAFE_OPS:
            return SAFE_OPS[type(node.op)](self._eval_node(node.operand))
        raise ValueError(f"Unsupported expression: {ast.dump(node)}")

    def calculate(self, expression: str) -> dict | str:
        """Evaluate a mathematical expression and return the result."""
        try:
            tree = ast.parse(expression, mode="eval")
            result = self._eval_node(tree)
            return {"result": result}
        except Exception as e:
            return f"Error: {str(e)}"