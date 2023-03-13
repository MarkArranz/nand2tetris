from enum import Enum, auto


class CommandType(Enum):
    C_ARITHMETIC = auto()
    C_PUSH = auto()
    C_POP = auto()
    C_LABEL = auto()
    C_GOTO = auto()
    C_IF = auto()
    C_FUNCTION = auto()
    C_RETURN = auto()
    C_CALL = auto()


COMMAND_TYPE_MAP = {
    "push": CommandType.C_PUSH,
    "pop": CommandType.C_POP,
    "add": CommandType.C_ARITHMETIC,
    "sub": CommandType.C_ARITHMETIC,
    "neg": CommandType.C_ARITHMETIC,
    "eq": CommandType.C_ARITHMETIC,
    "gt": CommandType.C_ARITHMETIC,
    "lt": CommandType.C_ARITHMETIC,
    "and": CommandType.C_ARITHMETIC,
    "or": CommandType.C_ARITHMETIC,
    "not": CommandType.C_ARITHMETIC,
}

COMMENT_TOKEN = "//"

SEGMENT_SYMBOLS = {
    "local": "LCL",
    "argument": "ARG",
    "this": "THIS",
    "that": "THAT",
    "temp": "TEMP",
}
