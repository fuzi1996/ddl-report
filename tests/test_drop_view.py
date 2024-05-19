import unittest

from generator import Generate
from parse.parser import Parser


class TestParseDropTable(unittest.TestCase):
    def test(self):
        table_name = "a1"
        sql = f"drop view {table_name};"
        parse = Parser()
        parse.parse(sql)
        parse_result = parse.get_parse_result()
        drop_tables = parse_result.get_drop_tables()
        self.assertEqual(len(drop_tables), 0)
        drop_views = parse_result.get_drop_views()
        self.assertEqual(len(drop_views), 1)
        self.assertEqual(drop_views[0], table_name)


class TestDropTableGenerate(unittest.TestCase):
    def test_drop_table(self):
        sql = """
            DROP view table_1;
        """
        parse = Parser()
        parse.parse(sql)
        parse_result = parse.get_parse_result()
        print(Generate.generate(parse_result))
