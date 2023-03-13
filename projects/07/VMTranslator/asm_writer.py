from constants import SEGMENT_SYMBOLS, CommandType


class CodeWriter:
    def __init__(self, output_file: str) -> None:
        """
        Opens an output file / stream and gets ready to write into it.
        """
        self._out_file = open(output_file, "w")

    def write_arithmetic(self, seg: str, value: int) -> None:
        """
        Writes to the output file the assembly code that implements the given arithmetic-logical commands.
        """
        self._pop_to_D()
        self._decrement_SP()

        if "add" == seg:
            self._write("M=D+M")

        self._increment_SP()

    def write_push_pop(self, cmd: CommandType, seg: str, index: int) -> None:
        """
        Write to the output file the assembly code that implements the given push or pop command.
        """
        self._goto_seg_addr(seg, index)

        if CommandType.C_PUSH == cmd:
            if "constant" == seg:
                # move contant's value to D
                self._write("D=A")
            else:
                # move segment's value to D
                self._write("D=M")
            self._push_D()
        elif CommandType.C_POP == cmd:
            # store segment's address into D
            self._write("D=A")
            # go to a spare register
            self._write("@R13")
            # store the segment's address into the spare register
            self._write("M=D")

            self._pop_to_D()

            # go to the spare register
            self._write("@R13")
            # go to the segment's address
            self._write("A=M")
            # store D in segment's address
            self._write("M=D")
        else:
            raise Exception(f"Invalid push/pop command: {cmd}")

    def write_comment(self, comment: str) -> None:
        """
        Writes to the output file the comment provided.
        """
        self._write(f"// {comment}")

    def close(self) -> None:
        """
        Closes the output file/stream.
        """
        self._out_file.close()

    def _write(self, cmd: str) -> None:
        self._out_file.write(f"{cmd}\n")

    def _goto_seg_addr(self, seg: str, offset_or_const: int) -> None:
        if "constant" == seg:
            self._write(f"@{offset_or_const}")
        else:
            # go to address where segment's base index is kept
            self._write(f"@{SEGMENT_SYMBOLS.get(seg)}")
            # put the segment's base index in D-reg
            self._write("D=M")
            # load the offset into A-reg
            self._write(f"@{offset_or_const}")
            # go to the address of segment's base index + the offset
            self._write("A=D+A")

    def _increment_SP(self):
        # go to where stack pointer address is kept
        self._write("@SP")
        # increment the stack pointer's address value and go to new address
        self._write("AM=M+1")

    def _decrement_SP(self) -> None:
        # go to where stack pointer address is kept
        self._write("@SP")
        # decrement the stack pointer's address value and go to new address
        self._write("AM=M-1")

    def _push_D(self):
        # go to where stack pointer's address is kept
        self._write("@SP")
        # go to the stack pointer's address
        self._write("A=M")
        # store the value in D-reg into the stack pointer's address
        self._write("M=D")
        self._increment_SP()

    def _pop_to_D(self) -> None:
        self._decrement_SP()
        # store the value at the stack pointer's address into D-reg
        self._write("D=M")
