import logging

from sqlglot.expressions import *

log = logging.getLogger(__name__)


class DropColumnDesc:
    def __init__(self, expression: AlterTable, action: Drop):
        table = expression.find(Table)
        drop_column = action.find(Identifier)

        # 所属表
        self.table = table.name
        # 字段
        self.column = drop_column.name
