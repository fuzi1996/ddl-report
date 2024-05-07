import unittest
from typing import List

from generator import Generate
from parse.parser import Parser
from result.result import ParseResult


class TestParseCreateTable(unittest.TestCase):
    def test_create_table(self):
        sql = """
            create view v_view as (select * from a_table)
        """
        parse = Parser()
        parse.parse(sql)
        parse_result = parse.get_parse_result()
        views: List[str] = parse_result.get_create_view()
        self.assertEqual(len(views), 1)

        view = views[0]
        self.assertEqual(view, "v_view")


class TestCreateViewGenerator(unittest.TestCase):
    def test_create_view(self):
        parse_result = ParseResult()
        parse_result.append_create_view("a_view")
        parse_result.append_create_view("b_view")
        parse_result.append_create_view("c_view")
        print(Generate.generate(parse_result))
