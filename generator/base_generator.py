from result.result import ParseResult


class BaseGenerator:
    def __init__(self, parse_result: ParseResult):
        self.parse_result = parse_result

    def generate(self) -> str:
        pass
