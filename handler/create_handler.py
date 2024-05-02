from sqlglot.expressions import *

from handler.expression_handler import ExpressionHandler
from result.create_table_desc import CreateTableDesc
from result.index_desc import IndexDescWrap


class CreateHandler(ExpressionHandler):

    def del_expression(self, expression: Create):
        if expression.kind.__eq__("VIEW"):
            identifier = expression.find(Identifier)
            self.parse_result.append_create_view(identifier.name)
        elif expression.kind.__eq__("INDEX"):
            index = IndexDescWrap.parse(expression)
            self.parse_result.append_add_index(index)
        else:
            desc = CreateTableDesc(expression)
            self.parse_result.append_create_table(desc)
