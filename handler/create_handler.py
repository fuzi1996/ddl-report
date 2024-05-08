from sqlglot.expressions import *

from handler.expression_handler import ExpressionHandler
from result.create_table_desc import CreateTableDesc
from result.index_desc import IndexDescWrap
from result.sql_wrapper import SqlWrapper


class CreateHandler(ExpressionHandler):

    def del_expression(self, sqlWrapper: SqlWrapper) -> None:
        expression = sqlWrapper.expression
        if not isinstance(expression, Select):
            if expression.kind.__eq__("VIEW"):
                identifier = expression.find(Identifier)
                self.parse_result.append_create_view(identifier.name)
            elif expression.kind.__eq__("INDEX"):
                index = IndexDescWrap.parse(expression)
                self.parse_result.append_add_index(index)
            else:
                desc = CreateTableDesc(expression)
                if len(desc.columns) > 0:
                    self.parse_result.append_create_table(desc)
                else:
                    # create table as select 忽略
                    pass
        else:
            self.parse_result.append_cant_parse(sqlWrapper.sql)
