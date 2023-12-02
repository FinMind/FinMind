from enum import Enum


class Rule(str, Enum):
    MoreThan = ">"
    LessThan = "<"
    Equal = "="
