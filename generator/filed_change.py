from typing import List, Dict

from generator.base_generator import BaseGenerator
from result.add_column_desc import AddColumnDesc
from result.alter_column_type_desc import AlterColumnTypeDesc
from result.drop_column_desc import DropColumnDesc


class FiledChange(BaseGenerator):

    def generate_add_columns(self) -> str:
        columns: List[AddColumnDesc] = self.parse_result.get_add_columns()

        if len(columns) > 0:
            column_descs = []
            for column in columns:
                table_name = column.table
                column_name = column.column
                column_type = column.type
                column_comment = self.parse_result.get_column_comment(table_name, column_name) or ""
                column_descs.append(f"| {table_name} | {column_name} | {column_type} | {column_comment} |")
            column_desc_str = "\n".join(column_descs)
            return f"""| 表 | 字段 | 类型 | 备注 |
| --- | --- | --- | --- |
{column_desc_str}            
            """
        else:
            return "无"

    def generate_drop_columns(self) -> str:
        drop_columns: List[DropColumnDesc] = self.parse_result.get_drop_columns()
        if len(drop_columns) > 0:
            drop_column_str = '\n'.join(
                [f'| {drop_column.table} | {drop_column.column} |' for drop_column in drop_columns])
            return f"""| 表 | 字段 | 备注 |
| --- | --- | --- |
{drop_column_str}
            """
        else:
            return "无"

    def generate_alter_column_types(self) -> str:
        alter_column_types: List[AlterColumnTypeDesc] = self.parse_result.get_alter_column_types()
        if len(alter_column_types) > 0:
            alter_column_type_strs = []
            for alter_column_type in alter_column_types:
                table_name = alter_column_type.table
                column_name = alter_column_type.column
                column_type = alter_column_type.type
                alter_column_type_strs.append(f"| {table_name} | {column_name} | {column_type} |")
            result = "\n".join(alter_column_type_strs)
            return f"""| 表 | 字段 | 修改后类型 |
| --- | --- | --- |
{result}
            """
        else:
            return "无"

    def generate_rename_column(self) -> str:
        rename_columns: Dict[str, Dict[str, str]] = self.parse_result.get_rename_columns()
        if len(rename_columns) > 0:
            rename_column_type_strs = []
            for table, rename_columns in rename_columns.items():
                for old_column, new_column in rename_columns.items():
                    rename_column_type_strs.append(f"| {table} | {old_column} | {new_column} |")
            result = "\n".join(rename_column_type_strs)
            return f"""| 表 | 原字段 | 修改后新字段 |
| --- | --- | --- |
{result}
            """
        else:
            return "无"

    def generate(self) -> str:
        add_columns = self.generate_add_columns()
        drop_columns = self.generate_drop_columns()
        alter_column_type = self.generate_alter_column_types()
        rename_columns = self.generate_rename_column()

        return f"""
## 字段

### 字段新增

{add_columns}

### 字段删除

{drop_columns}

### 字段重命名

{rename_columns}

### 字段类型修改

{alter_column_type}
    """
