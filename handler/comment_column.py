from sqlglot.expressions import *

from handler.expression_handler import ExpressionHandler


class CommentColumn(ExpressionHandler):
    def del_expression(self, expression: Expression):
        comment_literal = expression.find(Literal)
        comment = expression.find(Comment)
        comment_this: Column = comment.args.get('this')
        table = comment_this.table
        column = comment_this.name
        self.parse_result.append_column_comment(table, column, comment_literal.name)
