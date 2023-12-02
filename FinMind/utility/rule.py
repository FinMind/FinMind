def more_than(x: float, y: float) -> bool:
    return x > y


def less_than(x: float, y: float) -> bool:
    return x < y


def equal(x: float, y: float) -> bool:
    return x == y


RULE_DICT = {
    "more_than": more_than,
    "less_than": less_than,
    "equal": equal,
    ">": more_than,
    "<": less_than,
    "=": equal,
}
