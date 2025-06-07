from polygon.ast.expressions.expression import Expression
from polygon.ast.node import Node

class IfExpression(Expression):
    def __init__(self, condition: Expression, true_expr: Expression, false_expr: Expression):
        self.condition = condition
        self.true_expr = true_expr
        self.false_expr = false_expr
        super().__init__(operator='if', args=[condition, true_expr, false_expr])

    def __str__(self):
        return f"IF({self.condition}, {self.true_expr}, {self.false_expr})"