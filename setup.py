from setuptools import setup

setup(
    name="ddl-report",
    description="An easily generate SQL ddl report",
    python_requires=">=3.7",
    install_requires=[
        'sqlglot==23.12.2'
    ]
)
