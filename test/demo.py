import sqlglot

import dialect.postgres

if __name__ == '__main__':
    sql = """
    create view v_view as (select * from a_table)
    """
    expressions = sqlglot.parse(sql, dialect=dialect.postgres.Postgres)
    expression = expressions[0]
    print(repr(expression))
    print(expression.sql())
