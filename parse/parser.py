import logging

import sqlglot
from sqlglot.expressions import *

import dialect.postgres
import handler.alter_table
from handler.comment_handler import CommentHandler
from handler.create_handler import CreateHandler
from handler.drop_table import DropTable
from result.result import ParseResult
from result.sql_wrapper import SqlWrapper

log = logging.getLogger(__name__)


class Parser:
    def __init__(self, **opts):
        self.debug = opts.get('debug', False)
        self._parse_result = ParseResult()
        self._create_handler = CreateHandler(self._parse_result)
        self._drop_table = DropTable(self._parse_result)
        self._alter_table = handler.alter_table.AlterTable(self._parse_result)
        self._comment_handler = handler.comment_handler.CommentHandler(self._parse_result)

    def parse(self, wrapper_or_sql_str: SqlWrapper or str):
        if wrapper_or_sql_str is None:
            raise Exception('sql cannot be None')

        is_wrapper = isinstance(wrapper_or_sql_str, SqlWrapper)

        if is_wrapper:
            wrapper: SqlWrapper = wrapper_or_sql_str
        else:
            wrapper = SqlWrapper(wrapper_or_sql_str, None)

        sql_str: str = wrapper.sql

        trip_sql = sql_str.strip()
        is_annotate = trip_sql.startswith("--")
        is_empty = trip_sql.__eq__("")
        if is_annotate or is_empty:
            if is_annotate:
                log.info(
                    f"正在解析 {wrapper.file_name} 文件中 {sql_str} 为注释,已忽略" if wrapper.file_name else f"正在解析 {sql_str} 为注释,已忽略")
        else:
            if self.debug:
                log.debug(
                    f"正在解析 {wrapper.file_name} 文件中 {sql_str}" if wrapper.file_name else f"正在解析 {sql_str}")

            expression = sqlglot.parse_one(sql_str, dialect=dialect.postgres.Postgres)

            wrapper.set_expression(expression)

            if expression is not None:
                if self.debug:
                    print(repr(expression))

                if isinstance(expression, Drop):
                    self._drop_table.del_expression(wrapper)
                elif isinstance(expression, AlterTable):
                    self._alter_table.del_expression(wrapper)
                elif isinstance(expression, Comment):
                    self._comment_handler.del_expression(wrapper)
                elif isinstance(expression, sqlglot.expressions.Create):
                    self._create_handler.del_expression(wrapper)
                elif (isinstance(expression, Delete)
                      or isinstance(expression, Update)
                      or isinstance(expression, Select)
                      or isinstance(expression, Insert)):
                    pass
                else:
                    self._parse_result.append_cant_parse(sql_str)

    def get_parse_result(self) -> ParseResult:
        return self._parse_result
