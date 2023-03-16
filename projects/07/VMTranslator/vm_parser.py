from constants import COMMAND_TYPE_MAP, COMMENT_TOKEN, CommandType


class Parser:
    def __init__(self, input_file: str) -> None:
        """
        Opens the input file / stream, and gets ready to parse it.
        """
        self._file = open(input_file, "r")
        self._next_instr = self._find_next_instr()

        self.cur_instr: str = ""
        self._cmd_type: CommandType
        self._arg1: str
        self._arg2: int

    def advance(self) -> None:
        """
        Reads the next command from the input and makes it the current command.

        This routine should be called only if `has_more_lines` is true.

        Initially there is no current command.
        """
        self.cur_instr = self._next_instr
        self._next_instr = self._find_next_instr()

        cmd, *rest = self.cur_instr.split(" ", 3)
        self._cmd_type = COMMAND_TYPE_MAP[cmd]
        self._arg1, self._arg2 = (
            (str(rest[0]), int(rest[1])) if bool(rest) else (cmd, 0)
        )

        if self._arg2 < 0:
            raise Exception("Invalid index: {self._arg2}. Index must be >= 0.")

    @property
    def has_more_lines(self) -> bool:
        """
        Are there more lines in the input?
        """
        return bool(self._next_instr)

    @property
    def command_type(self) -> CommandType:
        """
        Returns a constant representing the type of the current command.

        If the current command is an arithmetic-logical command, returns C_ARITHMETIC.
        """
        return self._cmd_type

    @property
    def arg1(self) -> str:
        """
        Returns the first argument of the current command.

        In the case of C_ARITHMETIC, the command itself (add, sub, etc.)
        is returned.

        Should not be called if the current command is C_RETURN.
        """
        return self._arg1

    @property
    def arg2(self) -> int:
        """
        Returns the second argument of the current command.

        Should be called only if the current command is C_PUSH, C_POP, C_FUNCTION, or C_CALL.
        """
        return self._arg2

    def close_file(self) -> None:
        """
        Closes the output file/stream.
        """
        self._file.close()

    def _find_next_instr(self) -> str:
        while True:
            line = self._file.readline()

            if not len(line):
                self.close_file()
                return ""

            stipped_line = line.strip()
            if self._is_vm_cmd(stipped_line):
                return stipped_line

    def _is_vm_cmd(self, line: str) -> bool:
        return bool(line) and not line.startswith(COMMENT_TOKEN)
