from generator.cant_parse import CantParse
from generator.filed_change import FiledChange
from generator.header import Header
from generator.table_change import TableChange
from generator.view_change import ViewChange
from result.result import ParseResult


class Generate:
    @staticmethod
    def generate(pase_result: ParseResult) -> str:
        generators = []
        generators.append(Header(pase_result))
        generators.append(TableChange(pase_result))
        generators.append(FiledChange(pase_result))
        generators.append(ViewChange(pase_result))
        generators.append(CantParse(pase_result))

        return "".join([generator.generate() for generator in generators])
