import unittest

from parse.parser import Parser


class TestParseDropTable(unittest.TestCase):
    def test(self):
        table_name = "a1"
        sql = f"drop table {table_name};"
        parse = Parser(sql)
        parse.parse()
        parse_result = parse.get_parse_result()
        drop_tables = parse_result.get_drop_tables()
        self.assertEqual(len(drop_tables), 1)
        self.assertEqual(drop_tables[0], table_name)

    def test_with_schema(self):
        table_name = "a1"
        table_name_with_schema = f"s.{table_name}"
        sql = f"drop table {table_name_with_schema};"
        parse = Parser(sql)
        parse.parse()
        parse_result = parse.get_parse_result()
        drop_tables = parse_result.get_drop_tables()
        self.assertEqual(len(drop_tables), 1)
        self.assertEqual(drop_tables[0], table_name)

    def test_with_exists(self):
        table_name = "a1"
        sql = f"DROP TABLE IF EXISTS {table_name};"
        parse = Parser(sql)
        parse.parse()
        parse_result = parse.get_parse_result()
        drop_tables = parse_result.get_drop_tables()
        self.assertEqual(len(drop_tables), 1)
        self.assertEqual(drop_tables[0], table_name)


if __name__ == '__main__':
    unittest.main()
