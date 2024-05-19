import unittest

from generator import Generate
from parse.parser import Parser


class TestParseViewChange(unittest.TestCase):

    # 先建后删,互相抵消
    def test_create_and_drop(self):
        parse = Parser()
        parse.parse("create view v_view as (select * from a_table)")
        parse.parse("drop view v_view")

        parse_result = parse.get_parse_result()

        drop_views = parse_result.get_drop_views()
        self.assertEqual(len(drop_views), 0)

        create_views = parse_result.get_create_views()
        self.assertEqual(len(create_views), 0)

    # 先建后删,互相抵消
    def test_drop_and_create(self):
        parse = Parser()
        parse.parse("drop view v_view")
        parse.parse("create view v_view as (select * from a_table)")

        parse_result = parse.get_parse_result()

        drop_views = parse_result.get_drop_views()
        self.assertEqual(len(drop_views), 0)

        create_views = parse_result.get_create_views()
        self.assertEqual(len(create_views), 0)

        update_views = parse_result.get_update_views()
        self.assertEqual(len(update_views), 1)
        self.assertEqual(update_views[0], 'v_view')

    # 先建后删,互相抵消
    def test_drop_and_create2(self):
        parse = Parser()
        parse.parse("drop view v_view")
        parse.parse("create view v_view as (select * from a_table)")
        parse.parse("drop view v_view")

        parse_result = parse.get_parse_result()

        drop_views = parse_result.get_drop_views()
        self.assertEqual(len(drop_views), 0)

        create_views = parse_result.get_create_views()
        self.assertEqual(len(create_views), 0)


class TestViewChangeGenerate(unittest.TestCase):
    def test_drop_table(self):
        sql = """
            DROP view table_1;
        """
        parse = Parser()
        parse.parse(sql)
        parse_result = parse.get_parse_result()
        print(Generate.generate(parse_result))

    def test_drop_and_create(self):
        parse = Parser()
        parse.parse("drop view v_view")
        parse.parse("create view v_view as (select * from a_table)")

        parse_result = parse.get_parse_result()
        print(Generate.generate(parse_result))
