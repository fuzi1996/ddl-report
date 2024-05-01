import logging
from typing import List

from sqlglot.expressions import *

log = logging.getLogger(__name__)


class ConstraintDesc:
    def __init__(self, expression: AlterTable, action: AddConstraint):
        table = expression.find(Table)

        constraint = action.find(Constraint)

        primary_key = action.find(PrimaryKey)
        unique_column_constraint = action.find(UniqueColumnConstraint)

        # 约束名称
        self.name = constraint.name
        # 所属表
        self.table = table.name
        # 是否主键
        self.is_pk = primary_key is not None
        # 是否唯一索引
        self.is_unique = unique_column_constraint is not None
        # 对应 expression
        self.expression: AlterTable = expression
        # 涉及字段
        if self.is_pk:
            self.columns: List[str] = [field.sql() for field in primary_key.expressions]
        elif self.is_unique:
            self.columns: List[str] = [field.sql() for field in
                                       unique_column_constraint.find_all(Identifier)]
        else:
            raise Exception("Unexpected constraint")
