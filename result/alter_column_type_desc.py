from sqlglot.expressions import *

from log.log import get_logger

log = get_logger(__name__)


class AlterColumnTypeDesc:
    def __init__(self, expression: AlterTable, alter_column: AlterColumn):
        table = expression.find(Table)

        # 所属表
        self.table = table.name.lower()
        # 字段
        self.column = alter_column.name.lower()
        # 修改后类型
        dtype = alter_column.args.get('dtype')
        self.type = dtype.sql().lower()
        # 对应 expression
        self.expression: AlterTable = expression
