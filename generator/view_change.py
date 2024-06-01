from generator.base_generator import BaseGenerator


class ViewChange(BaseGenerator):
    def generate(self) -> str:
        create_views = self.parse_result.get_create_views()
        create_view_result = "无"
        if len(create_views) > 0:
            create_view_result = "\n".join([f"- {view}" for view in self.sort_list(create_views)])

        drop_views = self.parse_result.get_drop_views()
        drop_view_result = "无"
        if len(drop_views) > 0:
            drop_view_result = "\n".join([f"- {view}" for view in self.sort_list(drop_views)])

        update_views = self.parse_result.get_update_views()
        update_view_result = "无"
        if len(update_views) > 0:
            update_view_result = "\n".join([f"- {view}" for view in self.sort_list(update_views)])

        return f"""
## 视图

### 删除视图

{drop_view_result}

### 新增视图

{create_view_result}

### 更新视图

{update_view_result}
    """
