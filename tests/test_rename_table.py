import unittest
from typing import Dict

from generator import Generate
from parse.parser import Parser


class TestParseRenameTable(unittest.TestCase):
    def test_rename_table(self):
        sql = """
            alter table a rename to "b";
        """
        parse = Parser()
        parse.parse(sql)
        parse_result = parse.get_parse_result()
        rename_tables: Dict[str, str] = parse_result.get_rename_tables()
        self.assertEqual(len(rename_tables), 1)
        new_table = rename_tables.get('a')
        self.assertEqual(new_table, 'b')

    def test_rename_table_2(self):
        parse = Parser()
        parse.parse("alter table h rename to \"k\";")
        parse.parse("alter table h rename to \"p\";")
        parse.parse("alter table a rename to \"b\";")
        parse.parse("alter table b rename to \"c\";")
        parse.parse("alter table d rename to e;")
        parse_result = parse.get_parse_result()
        rename_tables = parse_result.get_rename_tables()
        self.assertEqual(len(rename_tables), 3)
        self.assertEqual(rename_tables.get('h'), 'p')
        self.assertEqual(rename_tables.get('a'), 'c')
        self.assertEqual(rename_tables.get('d'), 'e')


class TestRenameTableGenerator(unittest.TestCase):
    def test_rename_table(self):
        parse = Parser()
        parse.parse("alter table h rename to \"k\";")
        parse.parse("alter table h rename to \"p\";")
        parse.parse("alter table a rename to \"b\";")
        parse.parse("alter table b rename to \"c\";")
        parse.parse("alter table d rename to e;")
        parse_result = parse.get_parse_result()
        print(Generate.generate(parse_result))
