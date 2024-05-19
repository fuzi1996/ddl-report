from typing import List

from sqlglot.expressions import *

from log.log import get_logger

log = get_logger(__name__)


class IndexDesc:
    def __init__(self):
        # 名称
        self.name = ""
        # 所属表
        self.table = ""
        # 是否主键
        self.is_pk = False
        # 是否唯一索引
        self.is_unique = False
        # 对应 expression
        self.expression: Expression | None = None
        self.columns: List[str] = []


class IndexDescWrap:
    @staticmethod
    def parse(expression: Create) -> IndexDesc:
        index = IndexDesc()
        indexExpr = expression.find(Index)
        table = indexExpr.find(Table)
        index.name = indexExpr.name
        index.table = table.name
        index.is_pk = False
        index.is_unique = expression.args.get("unique") or False
        index.expression = expression

        indexParameters = expression.find(IndexParameters)
        for column in indexParameters.find_all(Column):
            index.columns.append(column.name)

        return index


class ConstraintDesc:

    @staticmethod
    def parse(expression: AlterTable, action: AddConstraint) -> IndexDesc:
        table = expression.find(Table)

        constraint = action.find(Constraint)

        primary_key = action.find(PrimaryKey)
        unique_column_constraint = action.find(UniqueColumnConstraint)

        index = IndexDesc()
        # 约束名称
        index.name = constraint.name
        # 所属表
        index.table = table.name
        # 是否主键
        index.is_pk = primary_key is not None
        # 是否唯一索引
        index.is_unique = unique_column_constraint is not None
        # 对应 expression
        index.expression = expression
        # 涉及字段
        if index.is_pk:
            index.columns = [field.sql() for field in primary_key.expressions]
        elif index.is_unique:
            index.columns = [field.sql() for field in
                             unique_column_constraint.find_all(Identifier)]
        else:
            raise Exception("Unexpected constraint")

        return index
