from generator.base_generator import BaseGenerator


class Header(BaseGenerator):
    def generate(self) -> str:
        return "# 数据结构变化\n\n"
