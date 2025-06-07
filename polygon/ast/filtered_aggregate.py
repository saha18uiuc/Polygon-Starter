from polygon.ast.expressions.expression import Expression

class FilteredAggregate(Expression):
    def __init__(self, aggregate, condition=None):
        self.aggregate = aggregate
        self.condition = condition
        super().__init__()
    
    def __str__(self):
        if self.condition:
            return f"{self.aggregate} FILTER (WHERE {self.condition})"
        return str(self.aggregate)