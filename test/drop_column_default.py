import unittest
from typing import List

from parse.parser import Parser
from result.drop_column_default_desc import DropColumnDefaultDesc


class TestParseDropColumn(unittest.TestCase):
    def test_drop_column_default(self):
        sql = """
            ALTER TABLE IF EXISTS a_table
                ALTER COLUMN id DROP DEFAULT;
        """
        parse = Parser(sql)
        parse.parse()
        parse_result = parse.get_parse_result()
        drop_column_defaults: List[DropColumnDefaultDesc] = parse_result.get_drop_column_defaults()
        self.assertEqual(len(drop_column_defaults), 1)
        drop_column_default = drop_column_defaults[0]
        self.assertEqual(drop_column_default.table, 'a_table')
        self.assertEqual(drop_column_default.column, 'id')


if __name__ == '__main__':
    unittest.main()
