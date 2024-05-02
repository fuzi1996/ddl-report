import unittest
from typing import List

from parse.parser import Parser
from result.alter_column_type_desc import AlterColumnTypeDesc


class TestParseAlterColumnType(unittest.TestCase):
    def test_alter_column_type(self):
        sql = """
            ALTER TABLE a_table ALTER COLUMN name1 TYPE character varying(300);
        """
        parse = Parser(sql)
        parse.parse()
        parse_result = parse.get_parse_result()
        alters: List[AlterColumnTypeDesc] = parse_result.get_alter_column_types()
        self.assertEqual(len(alters), 1)
        alter = alters[0]
        self.assertEqual(alter.table, 'a_table')
        self.assertEqual(alter.column, 'name1')
        self.assertEqual(alter.type, 'VARCHAR(300)')

    def test_alter_column_type(self):
        sql = """
              ALTER TABLE b_table
                ALTER COLUMN b_column TYPE text COLLATE "pg_catalog"."default" USING b_column::text;
        """
        parse = Parser(sql)
        parse.parse()
        expressions = parse.get_expressions()
        parse_result = parse.get_parse_result()
        alters: List[AlterColumnTypeDesc] = parse_result.get_alter_column_types()
        self.assertEqual(len(alters), 1)
        alter = alters[0]
        self.assertEqual(alter.table, 'b_table')
        self.assertEqual(alter.column, 'b_column')
        self.assertEqual(alter.type, 'TEXT')
