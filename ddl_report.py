"""
unsupported syntax:

ALTER TABLE a_table ALTER COLUMN a_type SET NOT NULL;
"""
import argparse
import glob
import logging
import os.path
from typing import List

from natsort import natsorted

from generator import Generate
from log.log import config_logging, get_logger
from parse.parser import Parser
from result.sql_wrapper import SqlWrapper

log = get_logger(__name__)

VERSION = "0.0.2"


def collect_sql_files(filepath: str) -> List[str]:
    is_dir = os.path.isdir(filepath)
    if is_dir:
        files = [file for file in glob.glob(os.path.join(filepath, "**", "*.sql"), recursive=True)]
    else:
        files = [filepath]
    return files


def read_sql_file(list: List[SqlWrapper], filepath: str):
    with open(filepath, "r", encoding='utf8') as f:
        read_content = f.read()
        lines = read_content.split('\n')
        filtered_lines = []
        for line in lines:
            if not line.startswith('--'):
                filtered_lines.append(line)
            else:
                log.info(f"{line} 为注释,已忽略")
        filtered_sql = "\n".join(filtered_lines)
        sql_lines = filtered_sql.split(";")

        for sql_line in sql_lines:
            if sql_line is not None and len(sql_line) > 0:
                list.append(SqlWrapper(sql_line, filepath))


if __name__ == '__main__':
    handlers = [logging.FileHandler(filename="ddl_report.log", mode="a", encoding="utf-8")]
    config_logging(logging.INFO, handlers=handlers)

    log.info(f"当前版本: {VERSION}")

    arg_parser = argparse.ArgumentParser(prog='DDL Report', description='解析SQL DDL,生成数据结构变动报告')
    arg_parser.add_argument('dir_path', help='sql文件所在目录,支持解析深层目录')
    arg_parser.add_argument('-o', '--output', default='数据结构变动.md', help='输出文件位置')
    arg_parser.add_argument('--verbose', default=False, action='store_true', help='是否输出调试信息')
    arg_parser.add_argument('-v', '--version', help='输出版本', action='version', version=f'%(prog)s {VERSION}')
    args = arg_parser.parse_args()

    dir_path = args.dir_path
    log.info(f"读取 {dir_path} 下所有sql文件")
    is_debug = args.verbose
    log.info(f"当前是否为 debug 模式: {is_debug}")
    output_path = args.output
    log.info(f"文件输出路径: {output_path}")

    sql_files = collect_sql_files(dir_path)
    wrapper_list: List[SqlWrapper] = []
    for sql_file in natsorted(sql_files):
        read_sql_file(wrapper_list, sql_file)

    parser = Parser(debug=is_debug)
    for wrapper in wrapper_list:
        parser.parse(wrapper)
    parse_result = parser.get_parse_result()
    report = Generate.generate(parse_result)
    open(output_path, 'wb').write(bytes(report, encoding='utf8'))
