from generator.base_generator import BaseGenerator
from result.create_table_desc import CreateTableDesc


class TableChange(BaseGenerator):

    def generate_create_table(self) -> str:
        create_tables = self.parse_result.get_create_tables()
        return "\n".join([self._generate_one_create_tables(create_table) for create_table in create_tables])

    def _generate_one_create_tables(self, create_table: CreateTableDesc) -> str:
        table_name = create_table.table
        table_comment = self.parse_result.get_table_comment(table_name) or ""
        create_table_header = f"{table_name(table_comment)}" if len(table_comment) > 0 else table_name
        columns = []
        for column_def in create_table.columns:
            column_name = column_def.column
            column_type = column_def.type
            column_comment = self.parse_result.get_column_comment(table_name, column_name) or ""
            columns.append(f"| {column_name} | {column_type} | {column_comment} |")
        column_descs = "\n".join(columns)

        return f"""#### {create_table_header}

| 字段 | 类型 | 备注 |
| --- | --- | --- |
{column_descs}
        """

    def generate_create_index(self) -> str:
        indexs = self.parse_result.get_add_indexs()
        if len(indexs) > 0:
            index_desc = []
            for index in indexs:
                index_name = index.name
                table_name = index.table
                index_comment = ""
                if index.is_pk:
                    index_comment = "主键"
                elif index.is_unique:
                    index_comment = "唯一索引"

                columns = index.columns
                if len(columns) > 1:
                    column_desc = ",".join([column for column in columns])
                    index_desc.append(f"| {index_name} | {table_name}({column_desc}) | {index_comment} |")
                else:
                    index_desc.append(f"| {index_name} | {table_name}.{columns[0]} | {index_comment} |")
            index_str = "\n".join(index_desc)
            return f"""| 索引名 | 对应字段 | 备注 |
| --- | --- | --- |
{index_str}
            """
        else:
            return "无"

    def generate_drop_table(self) -> str:
        tables = self.parse_result.get_drop_tables()
        return "无" if len(tables) > 0 else "\n".join([f"- {table}" for table in tables])

    def generate(self) -> str:
        create_table = self.generate_create_table() or "无"
        create_index = self.generate_create_index() or "无"
        drop_table = self.generate_drop_table() or "无"

        return f"""## 数据表

### 新建表

{create_table}

### 删除表

{drop_table}

### 新建索引

{create_index}
        """
