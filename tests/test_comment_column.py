import unittest
from typing import Dict

from parse.parser import Parser


class TestParseCommentColumn(unittest.TestCase):
    def test_comment_column(self):
        sql = """
            COMMENT ON COLUMN d_table.d_column IS '注释1';
        """
        parse = Parser()
        parse.parse(sql)
        parse_result = parse.get_parse_result()
        comments: Dict[str, Dict[str, str]] = parse_result.get_column_comments()
        self.assertEqual(len(comments), 1)
        column_comment = comments['d_table']
        self.assertIsNotNone(column_comment)
        self.assertEqual(column_comment['d_column'], '注释1')

    def test_repeat(self):
        sql = """
            COMMENT ON COLUMN d_table.d_column IS '注释1';
            COMMENT ON COLUMN d_table.d_column IS '注释2';
        """
        parse = Parser()
        parse.parse(sql)
        parse_result = parse.get_parse_result()
        comments: Dict[str, Dict[str, str]] = parse_result.get_column_comments()
        self.assertEqual(len(comments), 1)
        column_comment = comments['d_table']
        self.assertIsNotNone(column_comment)
        self.assertEqual(column_comment['d_column'], '注释1')

    def test_multi_comment(self):
        sql = """
            COMMENT ON COLUMN d_table.a_column IS '注释1';
            COMMENT ON COLUMN d_table.d_column IS '注释2';
        """
        parse = Parser()
        parse.parse(sql)
        parse_result = parse.get_parse_result()
        comments: Dict[str, Dict[str, str]] = parse_result.get_column_comments()
        self.assertEqual(len(comments), 1)
        column_comment = comments['d_table']
        self.assertIsNotNone(column_comment)
        self.assertEqual(column_comment['a_column'], '注释1')

        self.assertEqual(parse_result.get_column_comment("d_table", "a_column"), "注释1")
