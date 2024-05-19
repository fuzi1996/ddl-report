from sqlglot.expressions import *

from handler.expression_handler import ExpressionHandler
from log.log import get_logger
from result.create_table_desc import CreateTableDesc
from result.index_desc import IndexDescWrap
from result.sql_wrapper import SqlWrapper

log = get_logger(__name__)


class CreateHandler(ExpressionHandler):

    def del_expression(self, sqlWrapper: SqlWrapper) -> None:
        expression = sqlWrapper.expression
        if not isinstance(expression, Select):
            if expression.kind.__eq__("VIEW"):
                identifier = expression.find(Identifier)
                view_name = identifier.name
                self._del_create_view(view_name)
            elif expression.kind.__eq__("INDEX"):
                index = IndexDescWrap.parse(expression)
                self.parse_result.append_add_index(index)
            else:
                desc = CreateTableDesc(expression)
                if len(desc.columns) > 0:
                    self.parse_result.append_create_table(desc)
                else:
                    # create table as select 备份表忽略
                    pass
        else:
            self.parse_result.append_cant_parse(sqlWrapper.sql)

    def _del_create_view(self, view_name: str) -> None:
        if self.parse_result.is_view_droped(view_name):
            self.parse_result.clean_view_droped_record(view_name)
            log.info(f"视图 {view_name} 先删除后创建,互相抵消,视为试图更新")
            # 试图更新
            self.parse_result.append_update_view(view_name)
        else:
            self.parse_result.append_create_view(view_name)
