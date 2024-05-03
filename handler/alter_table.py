from typing import List

from sqlglot.expressions import *

from handler.expression_handler import ExpressionHandler
from result.add_column_desc import AddColumnDesc
from result.alter_column_type_desc import AlterColumnTypeDesc
from result.drop_column_desc import DropColumnDesc
from result.index_desc import ConstraintDesc


# table ddl
class AlterTable(ExpressionHandler):

    def del_expression(self, expression: Expression):
        actions: List[Expression] = expression.args.get('actions')
        if len(actions) > 0:
            for action in actions:
                if isinstance(action, AddConstraint):
                    index = ConstraintDesc.parse(expression, action)
                    self.parse_result.append_add_index(index)
                elif isinstance(action, AlterColumn):
                    alter_column = action.find(AlterColumn)
                    dtype = alter_column.args.get('dtype')
                    drop = alter_column.args.get('drop')
                    alter_column.sql()
                    if dtype is not None:
                        alter = AlterColumnTypeDesc(expression, alter_column)
                        self.parse_result.append_alter_column_type(alter)
                    elif drop is not None:
                        desc = DropColumnDesc(expression, alter_column)
                        self.parse_result.append_drop_column_default(desc)
                    else:
                        self.parse_result.append_cant_parse(expression.sql())
                elif isinstance(action, Drop):
                    drop_column = DropColumnDesc(expression, action)
                    self.parse_result.append_drop_column(drop_column)
                elif isinstance(action, ColumnDef):
                    add_column = AddColumnDesc(expression, action)
                    self.parse_result.append_add_column(add_column)
                else:
                    self.parse_result.append_cant_parse(expression.sql())
        else:
            self.parse_result.append_cant_parse(expression.sql())
