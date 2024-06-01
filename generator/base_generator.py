from typing import List, Dict

from natsort import natsorted

from result.result import ParseResult


def sort_dict(value: Dict):
    return dict(sorted(value.items(), key=lambda item: item[0]))


def sort_list(list: List, *attr_names: str):
    def sort(obj):
        values = []
        if len(attr_names) == 0:
            values.append(obj)
        else:
            for attr_name in attr_names:
                value = getattr(obj, attr_name)
                values.append(value)
        return tuple(values)

    return natsorted(list, key=sort)


class BaseGenerator:
    def __init__(self, parse_result: ParseResult):
        self.parse_result = parse_result

    def generate(self) -> str:
        pass

    def sort_list(self, list: List, *attr_names: str) -> List:
        return sort_list(list, *attr_names)

    def sort_dict(self, dict: Dict) -> Dict:
        return sort_dict(dict)
