from sqlglot.expressions import *

from handler.expression_handler import ExpressionHandler
from result.sql_wrapper import SqlWrapper


class CommentHandler(ExpressionHandler):
    def del_expression(self, sqlWrapper: SqlWrapper) -> None:
        expression = sqlWrapper.expression
        comment_literal = expression.find(Literal)
        comment = expression.find(Comment)
        comment_this: Column = comment.args.get('this')
        if comment_this.key.__eq__("column"):
            table = comment_this.table
            column = comment_this.name
            self.parse_result.append_column_comment(table, column, comment_literal.name)
        elif comment_this.key.__eq__("table"):
            self.parse_result.put_table_column(comment_this.name, comment_literal.name)
        else:
            self.parse_result.append_cant_parse(sqlWrapper.sql)
