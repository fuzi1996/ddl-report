import unittest
from typing import List

from generator import Generate
from parse.parser import Parser
from result.result import ParseResult


class TestCantParseSql(unittest.TestCase):
    def test_cant_parse_sql(self):
        sql = """
            ALTER TABLE a_table ALTER COLUMN a_type SET NOT NULL;
        """
        parse = Parser()
        parse.parse(sql)
        parse_result = parse.get_parse_result()
        sqls: List[str] = parse_result.get_cant_parse()
        self.assertEqual(len(sqls), 1)
        sql0 = sqls[0]
        self.assertEqual(sql0, 'ALTER TABLE a_table ALTER COLUMN a_type DROP DEFAULT, SET NOT NULL')


class TestCantParseGenerator(unittest.TestCase):
    def test_cant_parse(self):
        parse_result = ParseResult()
        parse_result.append_cant_parse("select f a_view")
        parse_result.append_cant_parse("alter 1")
        print(Generate.generate(parse_result))
