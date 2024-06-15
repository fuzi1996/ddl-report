import unittest
from typing import List

from ddl_report import read_sqls
from parse.parser import Parser
from result.sql_wrapper import SqlWrapper

class BaseTest(unittest.TestCase):
    def parse_sqls(self, sql: str, is_debug: bool = False) -> Parser:
        wrapper_list: List[SqlWrapper] = []
        read_sqls(sql, wrapper_list, "")

        parser = Parser(debug=is_debug)
        for wrapper in wrapper_list:
            parser.parse(wrapper)
        return parser
