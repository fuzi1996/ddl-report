import logging

from sqlglot.expressions import *

log = logging.getLogger(__name__)


class AddColumnDesc():
    def __init__(self, expression: AlterTable, action: ColumnDef):
        table = expression.find(Table)

        # 所属表
        self.table = table.name
        # 字段
        self.column = action.name
        # 类型
        dtype = action.args.get('kind')
        self.type = dtype.sql()
        # 对应 expression
        self.expression: AlterTable = expression
