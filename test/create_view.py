import unittest
from typing import List

from parse.parser import Parser


class TestParseCreateTable(unittest.TestCase):
    def test_create_table(self):
        sql = """
            create view v_view as (select * from a_table)
        """
        parse = Parser(sql)
        parse.parse()
        parse_result = parse.get_parse_result()
        views: List[str] = parse_result.get_create_view()
        self.assertEqual(len(views), 1)

        view = views[0]
        self.assertEqual(view, "v_view")
