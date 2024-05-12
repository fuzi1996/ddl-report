from setuptools import setup, find_packages

setup(
    name="ddl-report",
    description="An easily generate SQL ddl report",
    packages=find_packages(include=["dialect", "generator", "handler", "parse", "result"]),
    python_requires=">=3.7",
    install_requires=[
        'sqlglot==23.12.2'
    ],
    entry_points={
        'console_scripts': [
            'ddl-report = ddl_report.__main__'
        ]
    }
)
