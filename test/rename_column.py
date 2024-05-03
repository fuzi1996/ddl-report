import unittest
from typing import Dict

from generator import Generate
from parse.parser import Parser


class TestParseRenameColumn(unittest.TestCase):
    def test_rename_column(self):
        sql = """
            ALTER TABLE table_name 
                RENAME COLUMN column_name TO new_column_name;
        """
        parse = Parser(sql)
        parse.parse()
        parse_result = parse.get_parse_result()
        rename_columns: Dict[str, Dict[str, str]] = parse_result.get_rename_columns()
        self.assertEqual(len(rename_columns), 1)
        table = rename_columns.get("table_name")
        self.assertEqual(table.get("column_name"), 'new_column_name')


class TestRenameColumneGenerate(unittest.TestCase):
    def test_rename_column(self):
        sql = """
            ALTER TABLE table_name 
                RENAME COLUMN column_name TO new_column_name;
            ALTER TABLE table_name 
                RENAME COLUMN column_name_1 TO new_column_name_2;
        """
        parse = Parser(sql)
        parse.parse()
        parse_result = parse.get_parse_result()
        print(Generate.generate(parse_result))
