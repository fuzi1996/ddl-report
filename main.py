"""
unsupported syntax:

ALTER TABLE a_table ALTER COLUMN a_type SET NOT NULL;
"""
import argparse
import glob
import os.path
from typing import List

from natsort import natsorted

from generator import Generate
from parse.parser import Parser
from result.sql_wrapper import SqlWrapper


def collect_sql_files(filepath: str) -> List[str]:
    is_dir = os.path.isdir(filepath)
    if is_dir:
        files = [file for file in glob.glob(os.path.join(filepath, "**", "*.sql"), recursive=True)]
    else:
        files = [filepath]
    return files


def read_sql_file(list: List[SqlWrapper], filepath: str):
    with open(filepath, "r", encoding='utf8') as f:
        sql_lines = f.read().split(";")
        for sql_line in sql_lines:
            if sql_line is not None and len(sql_line) > 0:
                list.append(SqlWrapper(sql_line, filepath))


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(prog='DDL Report', description='解析SQL DDL,生成数据结构变动报告')
    arg_parser.add_argument('filepath')
    args = arg_parser.parse_args()

    filepath = args.filepath
    sql_files = collect_sql_files(filepath)
    wrapper_list: List[SqlWrapper] = []
    for sql_file in natsorted(sql_files):
        read_sql_file(wrapper_list, sql_file)

    parser = Parser()
    for wrapper in wrapper_list:
        parser.parse(wrapper)
    parse_result = parser.get_parse_result()
    report = Generate.generate(parse_result)
    print(report)
