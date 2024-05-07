from result.result import ParseResult
from result.sql_wrapper import SqlWrapper


class ExpressionHandler:
    def __init__(self, parse_result: ParseResult):
        self.parse_result = parse_result

    def del_expression(self, sqlWrapper: SqlWrapper) -> None:
        pass
