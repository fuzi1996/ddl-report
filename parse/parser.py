import logging
from typing import List

import sqlglot
from sqlglot.expressions import *

import dialect.postgres
import handler.alter_table
from handler.comment_column import CommentColumn
from handler.createhandler import CreateHandler
from handler.drop_table import DropTable
from result.result import ParseResult

log = logging.getLogger(__name__)


class Parser:
    def __init__(self, sql, **opts):
        if sql is None:
            raise Exception('sql cannot be None')
        self.sql = sql
        self.debug = opts.get('debug', False)

        self._expressions: Expression | None = None

        self._parse_result = ParseResult()
        self._create_table = CreateHandler(self._parse_result)
        self._drop_table = DropTable(self._parse_result)
        self._alter_table = handler.alter_table.AlterTable(self._parse_result)
        self._comment_column = handler.comment_column.CommentColumn(self._parse_result)

    def _parse_(self):
        self._expressions = sqlglot.parse(self.sql, dialect=dialect.postgres.Postgres)

    def parse(self):
        self._parse_()

        for expression in self._expressions:

            if self.debug:
                print(repr(expression))

            if isinstance(expression, Drop):
                self._drop_table.del_expression(expression)
            elif isinstance(expression, AlterTable):
                self._alter_table.del_expression(expression)
            elif isinstance(expression, Comment):
                self._comment_column.del_expression(expression)
            elif isinstance(expression, sqlglot.expressions.Create):
                self._create_table.del_expression(expression)
            else:
                self._parse_result.append_cant_parse(expression.sql())

    def get_parse_result(self) -> ParseResult:
        return self._parse_result

    def get_expressions(self) -> List[Expression]:
        return self._expressions
