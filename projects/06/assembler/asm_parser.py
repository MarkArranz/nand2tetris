import re

from hack_types import InstructionType, LineType


class AsmParser:
    def __init__(self):
        self.line_type: LineType
        self.instruction: str
        self.instruction_type: InstructionType | None
        self.dest: str
        self.comp: str
        self.jump: str

    def parse(self, text: str) -> None:
        # Is `text` a label description?
        if re.match(r"^\([A-Za-z_.$:][\w.$:]*\)$", text):
            self._parse_label_description(text)
            return None

        # Is `text` a numeric A-instruction or a symbolic A-instruction?`
        if re.match(r"^@\d+$", text) or re.match(r"^@[A-Za-z_.$:][\w.$:]*$", text):
            self._parse_a_instruction(text)
            return None

        # Is `text` a symbolic C-instruction?
        if "=" in text or ";" in text:
            self._parse_c_instruction(text)
            return None

        # Then what the heck is it!?
        raise SyntaxError("Malformed Hack assembly code.")

    def _parse_label_description(self, text: str) -> None:
        self.line_type = LineType.LABEL_DECLARATION
        self.instruction = text.strip("()")
        self.instruction_type = None
        self.dest = self.comp = self.jump = ""

    def _parse_c_instruction(self, text: str) -> None:
        self.line_type = LineType.ASSEMBLY_INSTRUCTION
        self.instruction_type = InstructionType.SYMBOLIC_C
        self.instruction = self.dest = self.comp = self.jump = ""

        if "=" in text:
            self.dest, self.comp = text.split("=")
        else:  # ";" in text
            self.comp, self.jump = text.split(";")

    def _parse_a_instruction(self, instr: str) -> None:
        self.line_type = LineType.ASSEMBLY_INSTRUCTION
        self.instruction = instr[1:]
        self.instruction_type = (
            InstructionType.NUMERIC_A
            if self.instruction.isdigit()
            else InstructionType.SYMBOLIC_A
        )
        self.dest = self.comp = self.jump = ""
