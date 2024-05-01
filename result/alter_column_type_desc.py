import logging

from sqlglot.expressions import *

log = logging.getLogger(__name__)


class AlterColumnTypeDesc:
    def __init__(self, expression: AlterTable, action: AlterColumn):
        table = expression.find(Table)
        alter_column = action.find(AlterColumn)

        # 所属表
        self.table = table.name
        # 字段
        self.column = alter_column.name
        # 修改后类型
        dtype = alter_column.args.get('dtype')
        self.type = dtype.sql()
        # 对应 expression
        self.expression: AlterTable = expression
