from generator.base_generator import BaseGenerator


class CantParse(BaseGenerator):
    def generate(self) -> str:
        cant_parse_sqls = self.parse_result.get_cant_parse()
        if len(cant_parse_sqls) > 0:
            sorted_value = self.sort_list(cant_parse_sqls)
            cant_parse_sql_str = "\n".join([f"- {cant_parse_sql.strip()}" for cant_parse_sql in sorted_value])
            return f"""## 无法解析SQL

{cant_parse_sql_str}
"""
        else:
            return ""
