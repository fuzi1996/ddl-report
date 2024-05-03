from generator.base_generator import BaseGenerator


class ViewChange(BaseGenerator):
    def generate(self) -> str:
        views = self.parse_result.get_create_view()
        result = "无"
        if len(views) > 0:
            result = "\n".join([f"- {view}" for view in views])
        return f"""

## 视图

### 新增视图

{result}

"""
