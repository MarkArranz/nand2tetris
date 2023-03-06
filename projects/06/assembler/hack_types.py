from enum import Enum, auto


class InstructionType(Enum):
    NUMERIC_A = auto()
    SYMBOLIC_A = auto()
    SYMBOLIC_C = auto()


class LineType(Enum):
    ASSEMBLY_INSTRUCTION = auto()
    LABEL_DECLARATION = auto()
