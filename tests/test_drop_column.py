import unittest
from typing import List

from generator import Generate
from parse.parser import Parser
from result.drop_column_desc import DropColumnDesc


class TestParseDropColumn(unittest.TestCase):
    def test_alter_column_type(self):
        sql = """
            ALTER TABLE "b_table"
                DROP COLUMN IF EXISTS "b_column";
        """
        parse = Parser()
        parse.parse(sql)
        parse_result = parse.get_parse_result()
        drop_columns: List[DropColumnDesc] = parse_result.get_drop_columns()
        self.assertEqual(len(drop_columns), 1)
        drop_column = drop_columns[0]
        self.assertEqual(drop_column.table, 'b_table')
        self.assertEqual(drop_column.column, 'b_column')


class TestDropColumnGenerator(unittest.TestCase):
    def test_drop_column(self):
        sql = """
            ALTER TABLE "b_table"
                DROP COLUMN IF EXISTS "b_column";    
            """
        parse = Parser()
        parse.parse(sql)
        parse_result = parse.get_parse_result()
        print(Generate.generate(parse_result))
