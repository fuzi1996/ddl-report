from typing import List, Dict

from log.log import get_logger
from result.add_column_desc import AddColumnDesc
from result.alter_column_type_desc import AlterColumnTypeDesc
from result.create_table_desc import CreateTableDesc
from result.drop_column_default_desc import DropColumnDefaultDesc
from result.drop_column_desc import DropColumnDesc
from result.index_desc import IndexDesc

log = get_logger(__name__)


class ParseResult:
    def __init__(self):
        self._create_tables: List[CreateTableDesc] = []

        self._drop_views: List[str] = []

        self._create_views: List[str] = []

        self._update_views: List[str] = []

        # 元素中每一项都是drop的表名
        self._drop_tables: List[str] = []

        # 元素中每一项都是无法解析的sql
        self._cant_parse: List[str] = []

        # 添加约束
        self._add_indexs: List[IndexDesc] = []

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
                old_column: new_column 
            }
        }
        """
        self._rename_columns: Dict[str, Dict[str, str]] = {}

        """
        {
            table_name: table_comment
        }
        """
        self._table_comments: Dict[str, str] = {}

        """
        {
            table_name: {
                column_name: column_comment 
            }
        }
        """
        self._column_comments: Dict[str, Dict[str, str]] = {}

    def get_create_tables(self) -> List[CreateTableDesc]:
        return self._create_tables

    def get_create_views(self) -> List[str]:
        return self._create_views

    def get_update_views(self) -> List[str]:
        return self._update_views

    def get_drop_views(self) -> List[str]:
        return self._drop_views

    def get_drop_tables(self) -> List[str]:
        return self._drop_tables

    def get_cant_parse(self) -> List[str]:
        return self._cant_parse

    def get_add_indexs(self) -> List[IndexDesc]:
        return self._add_indexs

    def get_alter_column_types(self) -> List[AlterColumnTypeDesc]:
        return self._alter_column_types

    def get_drop_columns(self) -> List[DropColumnDesc]:
        return self._drop_columns

    def get_add_columns(self) -> List[AddColumnDesc]:
        return self._add_columns

    def get_column_comments(self) -> Dict[str, Dict[str, str]]:
        return self._column_comments

    def get_table_comments(self) -> Dict[str, str]:
        return self._table_comments

    def get_rename_columns(self) -> Dict[str, Dict[str, str]]:
        return self._rename_columns

    def get_column_comment(self, table, column) -> str:
        table_dict = self._column_comments.get(table)
        if table_dict is not None:
            return table_dict.get(column) or ""
        return ""

    def get_table_comment(self, table) -> str:
        return self._table_comments.get(table) or ""

    def get_drop_column_defaults(self) -> List[DropColumnDefaultDesc]:
        return self._drop_column_defaults

    def append_create_table(self, desc: CreateTableDesc):
        table = desc.table
        for inner in self._create_tables:
            if inner.table.__eq__(table):
                log.warning(f"表 {table} 定义重复\nsql1: {inner.expression.sql()}\nsql2: {desc.expression.sql()}")
        self._create_tables.append(desc)

    def append_create_view(self, view: str):
        for inner in self._create_views:
            if inner.__eq__(view):
                log.warning(f"视图 {view} 定义重复")
        self._create_views.append(view)

    def is_view_created(self, view: str) -> bool:
        return view in self._create_views

    def clean_view_created_record(self, view: str):
        if view in self._create_views:
            self._create_views.remove(view)
        else:
            raise Exception(f'view {view} is not in created list,could not clean created record')

    def append_update_view(self, view: str):
        if view not in self._update_views:
            self.append_update_view(view)

    def is_view_updated(self, view: str) -> bool:
        return view in self._update_views

    def clean_view_updated_record(self, view: str):
        if view in self._update_views:
            self._update_views.remove(view)
        else:
            raise Exception(f'view {view} is not in updated list,could not clean updated record')

    def append_drop_view(self, view_name: str):
        if view_name not in self._drop_views:
            self._drop_views.append(view_name)

    def is_view_droped(self, view_name: str) -> bool:
        return view_name in self._drop_views

    def clean_view_droped_record(self, view_name: str):
        if view_name in self._drop_views:
            self._drop_views.remove(view_name)
        else:
            raise Exception(f'view {view_name} is not in droped list,could not clean droped record')

    def append_drop_table(self, table_name: str):
        if table_name not in self._drop_tables:
            self._drop_tables.append(table_name)

    def is_table_droped(self, table_name: str) -> bool:
        return table_name in self._drop_tables

    def append_cant_parse(self, sql):
        if sql not in self._cant_parse:
            self._cant_parse.append(sql)

    def append_add_index(self, index: IndexDesc):
        name = index.name
        table = index.table

        for inner_constraint in self._add_indexs:
            if inner_constraint.table.__eq__(table) and inner_constraint.name.__eq__(name):
                # 该表下已经存在同名约束
                log.warning(
                    f"""表 {table} 下约束 {name} 定义重复
sql1: {inner_constraint.expression.sql()}
sql2: {index.expression.sql()}""")
        self._add_indexs.append(index)

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

    def put_table_column(self, table, comment):
        table_comment = self._table_comments.get(table)
        if table_comment is None:
            self._table_comments[table] = comment
        else:
            if not table_comment.__eq__(comment):
                log.warning(f"表 {table} 注释定义重复 {table_comment} -> {comment}")
            self._table_comments[table] = comment

    def append_drop_column_default(self, desc: DropColumnDefaultDesc):
        table = desc.table
        column = desc.column
        for inner in self._drop_column_defaults:
            if inner.table.__eq__(table) and inner.column.__eq__(column):
                log.warning(f"表 {table} 字段 {column} 删除重复")
        self._drop_column_defaults.append(desc)

    def append_rename_column(self, table, old_column, new_column):
        table_dict = self._rename_columns.get(table)
        if table_dict is None:
            self._rename_columns[table] = {
                old_column: new_column
            }
        else:
            inner = table_dict.get(old_column)
            if inner is not None:
                log.warning(f"表 {table} 字段 {old_column} 重命名重复 {old_column} -> {new_column}")
            table_dict[old_column] = new_column
