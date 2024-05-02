from sqlglot.expressions import *

from handler.expression_handler import ExpressionHandler
from result.create_table_desc import CreateTableDesc


class CreateTable(ExpressionHandler):

    def del_expression(self, expression: Expression):
        desc = CreateTableDesc(expression)
        self.parse_result.append_create_table(desc)
