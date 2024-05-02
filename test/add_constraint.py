import unittest

from parse.parser import Parser


class TestParseAddConstraint(unittest.TestCase):
    def test_primary_key(self):
        sql = "ALTER TABLE persons ADD CONSTRAINT persons_pk PRIMARY KEY (first_name, last_name)"
        parse = Parser(sql)
        parse.parse()
        parse_result = parse.get_parse_result()
        constraints = parse_result.get_add_constraints()
        self.assertEqual(len(constraints), 1)
        constraint = constraints[0]
        self.assertEqual(constraint.name, "persons_pk")
        self.assertEqual(constraint.table, "persons")
        self.assertEqual(constraint.is_pk, True)
        self.assertEqual(constraint.is_unique, False)
        self.assertEqual(len(constraint.columns), 2)
        self.assertListEqual(constraint.columns, ["first_name", "last_name"])
        self.assertIsNotNone(constraint.expression)

    def test_repeat(self):
        sql = """
            ALTER TABLE persons ADD CONSTRAINT persons_pk PRIMARY KEY (first_name1, last_name);
            ALTER TABLE persons ADD CONSTRAINT persons_pk PRIMARY KEY (first_name2, last_name);
        """
        parse = Parser(sql)
        parse.parse()
        parse_result = parse.get_parse_result()
        constraints = parse_result.get_add_constraints()
        self.assertEqual(len(constraints), 2)
        constraint = constraints[0]
        self.assertEqual(constraint.name, "persons_pk")
        self.assertEqual(constraint.table, "persons")
        self.assertEqual(constraint.is_pk, True)
        self.assertEqual(constraint.is_unique, False)
        self.assertEqual(len(constraint.columns), 2)
        self.assertListEqual(constraint.columns, ["first_name1", "last_name"])
        self.assertIsNotNone(constraint.expression)

        constraint = constraints[1]
        self.assertEqual(constraint.name, "persons_pk")
        self.assertEqual(constraint.table, "persons")
        self.assertEqual(constraint.is_pk, True)
        self.assertEqual(constraint.is_unique, False)
        self.assertEqual(len(constraint.columns), 2)
        self.assertListEqual(constraint.columns, ["first_name2", "last_name"])
        self.assertIsNotNone(constraint.expression)

    def test_unique_constraint(self):
        sql = "ALTER TABLE ONLY risk ADD CONSTRAINT risk_uk UNIQUE (name);"
        parse = Parser(sql)
        parse.parse()
        parse_result = parse.get_parse_result()
        constraints = parse_result.get_add_constraints()
        self.assertEqual(len(constraints), 1)
        constraint = constraints[0]
        self.assertEqual(constraint.name, "risk_uk")
        self.assertEqual(constraint.table, "risk")
        self.assertEqual(constraint.is_pk, False)
        self.assertEqual(constraint.is_unique, True)
        self.assertEqual(len(constraint.columns), 1)
        self.assertListEqual(constraint.columns, ["name"])
        self.assertIsNotNone(constraint.expression)
