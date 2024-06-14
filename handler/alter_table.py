from typing import List

from sqlglot.expressions import *

from handler.expression_handler import ExpressionHandler
from result.add_column_desc import AddColumnDesc
from result.alter_column_type_desc import AlterColumnTypeDesc
from result.drop_column_desc import DropColumnDesc
from result.index_desc import ConstraintDesc
from result.sql_wrapper import SqlWrapper


# table ddl
class AlterTable(ExpressionHandler):

    def del_expression(self, sqlWrapper: SqlWrapper) -> None:
        expression = sqlWrapper.expression
        options: List[Expression] = expression.args.get('options')
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
                    action.args.get('options')
                    if dtype is not None:
                        alter = AlterColumnTypeDesc(expression, alter_column)
                        self.parse_result.append_alter_column_type(alter)
                    elif drop is not None:
                        desc = DropColumnDesc(expression, alter_column)
                        self.parse_result.append_drop_column_default(desc)
                    elif options is not None:
                        for option in options:
                            if isinstance(option, SetConfigProperty):
                                # ignore ALTER TABLE a_table ALTER COLUMN a_type SET NOT NULL;
                                pass
                            else:
                                self.parse_result.append_cant_parse(sqlWrapper.sql)
                    else:
                        self.parse_result.append_cant_parse(sqlWrapper.sql)
                elif isinstance(action, Drop):
                    drop_column = DropColumnDesc(expression, action)
                    self.parse_result.append_drop_column(drop_column)
                elif isinstance(action, ColumnDef):
                    add_column = AddColumnDesc(expression, action)
                    self.parse_result.append_add_column(add_column)
                elif isinstance(action, RenameColumn):
                    table = expression.find(Table)
                    old_column = action.args.get('this')
                    new_column = action.args.get('to')
                    table_name = table.name
                    self.parse_result.append_rename_column(table_name, old_column.name, new_column.name)
                elif isinstance(action, RenameTable):
                    table: Table = expression.args.get('this')
                    old_table: str = table.name
                    rename_table: RenameTable = expression.find(RenameTable)
                    new_table: Table = rename_table.args.get('this')
                    new_table_name = new_table.name
                    self.parse_result.append_rename_table(old_table, new_table_name)
                else:
                    self.parse_result.append_cant_parse(sqlWrapper.sql)
        else:
            self.parse_result.append_cant_parse(sqlWrapper.sql)
