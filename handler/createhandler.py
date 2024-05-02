from sqlglot.expressions import *

from handler.expression_handler import ExpressionHandler
from result.create_table_desc import CreateTableDesc


class CreateHandler(ExpressionHandler):

    def del_expression(self, expression: Create):
        if expression.kind.__eq__("VIEW"):
            identifier = expression.find(Identifier)
            self.parse_result.append_create_view(identifier.name)
        else:
            desc = CreateTableDesc(expression)
            self.parse_result.append_create_table(desc)
