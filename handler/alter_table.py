from typing import List

from sqlglot.expressions import *

from handler.expression_handler import ExpressionHandler
from result.add_column_desc import AddColumnDesc
from result.alter_column_type_desc import AlterColumnTypeDesc
from result.drop_column_desc import DropColumnDesc
from result.result import ConstraintDesc


# table ddl
class AlterTable(ExpressionHandler):

    def del_expression(self, expression: Expression):
        actions: List[Expression] = expression.args.get('actions')
        if len(actions) > 0:
            for action in actions:
                if isinstance(action, AddConstraint):
                    constraint = ConstraintDesc(expression, action)
                    self.parse_result.append_add_constraints(constraint)
                if isinstance(action, AlterColumn):
                    alter = AlterColumnTypeDesc(expression, action)
                    self.parse_result.append_alter_column_type(alter)
                if isinstance(action, Drop):
                    drop_column = DropColumnDesc(expression, action)
                    self.parse_result.append_drop_column(drop_column)
                if isinstance(action, ColumnDef):
                    add_column = AddColumnDesc(expression, action)
                    self.parse_result.append_add_column(add_column)
                else:
                    self.parse_result.append_cant_parse(expression.sql())
        else:
            self.parse_result.append_cant_parse(expression.sql())
