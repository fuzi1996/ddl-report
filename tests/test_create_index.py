import unittest

from generator import Generate
from parse.parser import Parser


class TestParseCreateIndex(unittest.TestCase):
    def test_create_index(self):
        sql = """
            create index i_index on a_table (code1,code2);
        """
        parse = Parser()
        parse.parse(sql)
        parse_result = parse.get_parse_result()
        indexs = parse_result.get_add_indexs()
        self.assertEqual(len(indexs), 1)
        index = indexs[0]
        self.assertEqual(index.table, "a_table")
        self.assertEqual(index.name, "i_index")
        self.assertEqual(index.is_pk, False)
        self.assertEqual(index.is_unique, False)
        self.assertListEqual(index.columns, ["code1", "code2"])

    def test_create_unique_index(self):
        sql = """
            create unique index i_index on a_table (code1,code2);
        """
        parse = Parser()
        parse.parse(sql)
        parse_result = parse.get_parse_result()
        indexs = parse_result.get_add_indexs()
        self.assertEqual(len(indexs), 1)
        index = indexs[0]
        self.assertEqual(index.table, "a_table")
        self.assertEqual(index.name, "i_index")
        self.assertEqual(index.is_pk, False)
        self.assertEqual(index.is_unique, True)
        self.assertListEqual(index.columns, ["code1", "code2"])


class TestCreateIndexGenerator(unittest.TestCase):
    def test_create_index(self):
        sql = """
            create index i_index on a_table (code1);
            create unique index i_index on a_table (code1,code2);
        """
        parse = Parser()
        parse.parse(sql)
        parse_result = parse.get_parse_result()
        print(Generate.generate(parse_result))
