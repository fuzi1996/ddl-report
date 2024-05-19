from sqlglot.expressions import *

from log.log import get_logger

log = get_logger(__name__)


class DropColumnDefaultDesc:
    def __init__(self, expression: AlterTable, action: Drop):
        table = expression.find(Table)
        drop_column = action.find(Identifier)

        # 所属表
        self.table = table.name
        # 字段
        self.column = drop_column.name
