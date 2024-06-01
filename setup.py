from setuptools import setup, find_packages

setup(
    name="ddl-report",
    description="An easily generate SQL ddl report",
    packages=find_packages(include=["dialect", "generator", "handler", "parse", "result", "log"]),
    python_requires=">=3.7",
    install_requires=[
        'sqlglot==24.1.0',
        'natsort==8.4.0'
    ]
)
