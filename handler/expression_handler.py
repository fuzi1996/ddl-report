from sqlglot.expressions import *

from result.result import ParseResult


class ExpressionHandler:
    def __init__(self, parse_result: ParseResult):
        self.parse_result = parse_result

    def del_expression(self, expression: Expression):
        pass
