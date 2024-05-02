import sqlglot

import dialect.postgres

if __name__ == '__main__':
    sql = """
    create UNIQUE index i_index
        on a_table (code);
    """
    expressions = sqlglot.parse(sql, dialect=dialect.postgres.Postgres)
    expression = expressions[0]
    print(repr(expression))
    print(expression.sql())
