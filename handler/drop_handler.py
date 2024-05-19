from sqlglot.expressions import *

from handler.expression_handler import ExpressionHandler
from log.log import get_logger
from result.sql_wrapper import SqlWrapper

log = get_logger(__name__)


# 删除表
class DropTableOrView(ExpressionHandler):

    def del_expression(self, sqlWrapper: SqlWrapper) -> None:
        expression: Expression = sqlWrapper.expression
        table = expression.find(Table)
        if table is not None:
            kind: str = expression.args.get('kind')
            if 'view'.__eq__(kind):
                self._del_drop_view(table.name)
            else:
                self.parse_result.append_drop_table(table.name)
        else:
            self.parse_result.append_cant_parse(sqlWrapper.sql)

    def _del_drop_view(self, view_name: str):
        if self.parse_result.is_view_created(view_name):
            self.parse_result.clean_view_created_record(view_name)
            log.info(f"视图 {view_name} 先建后删,互相抵消")
        elif self.parse_result.is_view_updated(view_name):
            self.parse_result.clean_view_updated_record(view_name)
            log.info(f"视图 {view_name} 先更新后删,互相抵消")
        else:
            # 之前没有创建过,添加删除记录
            self.parse_result.append_drop_view(view_name)
