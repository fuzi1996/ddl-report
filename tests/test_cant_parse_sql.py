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
        self.assertEqual(len(sqls), 0)


class TestCantParseGenerator(unittest.TestCase):
    def test_cant_parse(self):
        parse_result = ParseResult()
        parse_result.append_cant_parse("select f a_view")
        parse_result.append_cant_parse("alter 1")
        print(Generate.generate(parse_result))
