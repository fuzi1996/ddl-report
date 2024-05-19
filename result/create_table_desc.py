from typing import List

from sqlglot.expressions import *

from log.log import get_logger

log = get_logger(__name__)


class ColumnDesc:
    def __init__(self, column, type):
        self.column = column
        self.type = type


class CreateTableDesc():
    def __init__(self, expression: Create):
        table = expression.find(Table)

        # 所属表
        self.table = table.name
        # 字段
        self.columns: List[ColumnDesc] = []

        for column_def in expression.find_all(ColumnDef):
            self.columns.append(ColumnDesc(column_def.name, column_def.kind.sql()))

        # 对应 expression
        self.expression: Create = expression
