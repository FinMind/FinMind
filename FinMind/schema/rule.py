from enum import Enum


class Rule(str, Enum):
    MoreThan = "more_than"
    LessThan = "less_than"
    Equal = "equal"
