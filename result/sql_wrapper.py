from sqlglot import Expression


class SqlWrapper:
    def __init__(self, sql, file_name):
        self.sql = sql
        self.file_name = file_name
        self.expression: Expression or None = None

    def set_expression(self, expression: Expression) -> None:
        self.expression = expression
