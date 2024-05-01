import logging
from typing import List, Dict

from result.add_column_desc import AddColumnDesc
from result.alter_column_type_desc import AlterColumnTypeDesc
from result.constraint_desc import ConstraintDesc
from result.drop_column_default_desc import DropColumnDefaultDesc
from result.drop_column_desc import DropColumnDesc

log = logging.getLogger(__name__)


class ParseResult:
    def __init__(self):
        # 元素中每一项都是drop的表名
        self._drop_tables: List[str] = []

        # 元素中每一项都是无法解析的sql
        self._cant_parse: List[str] = []

        # 添加约束
        self._add_constraints: List[ConstraintDesc] = []

        # 字段类型修改
        self._alter_column_types: List[AlterColumnTypeDesc] = []

        # 字段删除默认值
        self._drop_column_defaults: List[DropColumnDefaultDesc] = []

        # 字段删除
        self._drop_columns: List[DropColumnDesc] = []

        # 字段新增
        self._add_columns: List[AddColumnDesc] = []

        """
        {
            table_name: {
                column_name: column_comment 
            }
        }
        """
        self._column_comments: Dict[str, Dict[str, str]] = {}

    def get_drop_tables(self) -> List[str]:
        return self._drop_tables

    def get_cant_parse(self) -> List[str]:
        return self._cant_parse

    def get_add_constraints(self) -> List[ConstraintDesc]:
        return self._add_constraints

    def get_alter_column_types(self) -> List[AlterColumnTypeDesc]:
        return self._alter_column_types

    def get_drop_columns(self) -> List[DropColumnDesc]:
        return self._drop_columns

    def get_add_columns(self) -> List[AddColumnDesc]:
        return self._add_columns

    def get_column_comments(self) -> Dict[str, Dict[str, str]]:
        return self._column_comments

    def get_drop_column_defaults(self) -> List[DropColumnDefaultDesc]:
        return self._drop_column_defaults

    def append_cant_parse(self, sql):
        if sql not in self._cant_parse:
            self._cant_parse.append(sql)

    def append_drop_table(self, table_name: str):
        if table_name not in self._drop_tables:
            self._drop_tables.append(table_name)

    def append_add_constraints(self, constraint: ConstraintDesc):
        name = constraint.name
        table = constraint.table

        for inner_constraint in self._add_constraints:
            if inner_constraint.table.__eq__(table) and inner_constraint.name.__eq__(name):
                # 该表下已经存在同名约束
                log.warning(
                    f"""表 {table} 下约束 {name} 定义重复
sql1: {inner_constraint.expression.sql()}
sql2: {constraint.expression.sql()}""")
        self._add_constraints.append(constraint)

    def append_alter_column_type(self, alter: AlterColumnTypeDesc):
        table = alter.table
        column = alter.column

        for inner_alter in self._alter_column_types:
            if inner_alter.table.__eq__(table) and inner_alter.column.__eq__(column):
                # 该表下已经存在同名约束
                log.warning(
                    f"表 {table} 下字段 {column} 类型修改重复\nsql1: {inner_alter.expression.sql()}\nsql2: {alter.expression.sql()}")
        self._alter_column_types.append(alter)

    def append_drop_column(self, drop_column: DropColumnDesc):
        table = drop_column.table
        column = drop_column.column

        for inner_drop_column in self._drop_columns:
            if inner_drop_column.table.__eq__(table) and inner_drop_column.column.__eq__(column):
                log.warning(
                    f"表 {table} 下字段 {column} 删除重复")
        self._drop_columns.append(drop_column)

    def append_add_column(self, add_column: AddColumnDesc):
        table = add_column.table
        column = add_column.column

        for inner_add_column in self._add_columns:
            if inner_add_column.table.__eq__(table) and inner_add_column.column.__eq__(column):
                log.warning(
                    f"表 {table} 下字段 {column} 新增重复\nsql1: {inner_add_column.expression.sql()}\nsql2: {add_column.expression.sql()}")
        self._add_columns.append(add_column)

    def append_column_comment(self, table, column, comment):
        table_dict = self._column_comments.get(table)
        if table_dict is None:
            self._column_comments[table] = {
                column: comment
            }
        else:
            inner_comment = table_dict.get(column)
            if inner_comment is not None:
                log.warning(f"表 {table} 字段 {column} 注释定义重复 {inner_comment} -> {comment}")

            table_dict[column] = comment

    def append_drop_column_default(self, desc: DropColumnDefaultDesc):
        table = desc.table
        column = desc.column
        for inner in self._drop_column_defaults:
            if inner.table.__eq__(table) and inner.column.__eq__(column):
                log.warning(f"表 {table} 字段 {column} 删除重复")
        self._drop_column_defaults.append(desc)
