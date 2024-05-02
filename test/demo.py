import sqlglot

import dialect.postgres

if __name__ == '__main__':
    sql = """create table a_table
        (
            column_1      int8,
            column_2      serial8,
            column_4      bool
        );
    """
    expressions = sqlglot.parse(sql, dialect=dialect.postgres.Postgres)
    # expressions = sqlglot.parse(sql, dialect="postgres")
    expression = expressions[0]
    print(repr(expression))
    print(expression.sql())
