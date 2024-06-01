from sqlglot.expressions import *

from log.log import get_logger

log = get_logger(__name__)


class AddColumnDesc():
    def __init__(self, expression: AlterTable, action: ColumnDef):
        table = expression.find(Table)

        # 所属表
        self.table = table.name.lower()
        # 字段
        self.column = action.name.lower()
        # 类型
        dtype = action.args.get('kind')
        self.type = dtype.sql().lower()
        # 对应 expression
        self.expression: AlterTable = expression
