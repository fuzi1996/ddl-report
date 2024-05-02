import unittest
from typing import List

from parse.parser import Parser
from result.create_table_desc import CreateTableDesc


class TestParseCreateTable(unittest.TestCase):
    def test_create_table(self):
        sql = """
            create table a_table
            (
                column_id      int8 not null constraint a_table_pk primary key,
                column_2       date,
                column_3       varchar(2000)
            );
        """
        parse = Parser(sql)
        parse.parse()
        parse_result = parse.get_parse_result()
        create_tables: List[CreateTableDesc] = parse_result.get_create_tables()
        self.assertEqual(len(create_tables), 1)

        create_table = create_tables[0]
        self.assertEqual(create_table.table, "a_table")
        columns = create_table.columns
        self.assertEqual(len(columns), 3)
        for column_def in columns:
            self.assertIn(column_def.column, ["column_id", "column_2", "column_3"])
            type = column_def.type
            if column_def.column == "column_id":
                self.assertEqual(type, "BIGINT")
            elif column_def.column == "column_2":
                self.assertEqual(type, "DATE")
            else:
                self.assertEqual(type, "VARCHAR(2000)")
