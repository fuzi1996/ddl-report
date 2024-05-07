from sqlglot.expressions import *

from handler.expression_handler import ExpressionHandler
from result.sql_wrapper import SqlWrapper


# 删除表
class DropTable(ExpressionHandler):

    def del_expression(self, sqlWrapper: SqlWrapper) -> None:
        expression = sqlWrapper.expression
        table = expression.find(Table)
        if table is not None:
            self.parse_result.append_drop_table(table.name)
        else:
            self.parse_result.append_cant_parse(sqlWrapper.sql)
