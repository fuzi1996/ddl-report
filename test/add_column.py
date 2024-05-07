import unittest
from typing import List

from generator import Generate
from parse.parser import Parser
from result.add_column_desc import AddColumnDesc


class TestParseAddColumn(unittest.TestCase):
    def test_add_column(self):
        sql = """
            ALTER TABLE IF EXISTS a_table
                ADD COLUMN a_column varchar(200);
        """
        parse = Parser()
        parse.parse(sql)
        parse_result = parse.get_parse_result()
        add_columns: List[AddColumnDesc] = parse_result.get_add_columns()
        self.assertEqual(len(add_columns), 1)
        add_column = add_columns[0]
        self.assertEqual(add_column.table, 'a_table')
        self.assertEqual(add_column.column, 'a_column')
        self.assertEqual(add_column.type, 'VARCHAR(200)')


class TestCreateTableGenerator(unittest.TestCase):
    def test_create_table(self):
        sql = """
            ALTER TABLE IF EXISTS a_table
                ADD COLUMN a_column varchar(200);    
            """
        parse = Parser()
        parse.parse(sql)
        parse_result = parse.get_parse_result()
        print(Generate.generate(parse_result))
