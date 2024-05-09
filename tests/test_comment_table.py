import unittest
from typing import Dict

from parse.parser import Parser


class TestParseCommentTable(unittest.TestCase):
    def test_comment_table(self):
        sql = """
            comment on table a_table is 'a table';
        """
        parse = Parser()
        parse.parse(sql)
        parse_result = parse.get_parse_result()
        comments: Dict[str, str] = parse_result.get_table_comments()
        self.assertEqual(len(comments), 1)
        self.assertEqual(comments.get("a_table"), 'a table')
