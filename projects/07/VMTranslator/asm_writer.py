from constants import (
    MAPPED_SEGMENTS,
    SYMBOLIC_SEGMENTS,
    CommandType,
)


class CodeWriter:
    def __init__(self, output_file: str) -> None:
        """
        Opens an output file / stream and gets ready to write into it.
        """
        self._out_file = open(output_file, "w")

        # This is used to create unique labels that mark conditional blocks of assembly.
        self._con_index = 0

    def write_arithmetic(self, op: str) -> None:
        """
        Writes to the output file the assembly code that implements the given arithmetic-logical commands.
        """
        if op not in ["neg", "not"]:
            self._pop_to_D()
        self._dec_SP()

        ## ARITHMETIC COMMANDS
        if "add" == op:
            self._write("M=D+M")
        elif "sub" == op:
            self._write("M=M-D")
        elif "neg" == op:
            self._write("M=-M")

        ## LOGICAL COMMANDS
        elif "and" == op:
            self._write("M=D&M")
        elif "or" == op:
            self._write("M=D|M")
        elif "not" == op:
            self._write("M=!M")

        ## CONDITIONAL LOGIC COMMANDS
        elif op in ["eq", "gt", "lt"]:
            # D = x - y
            self._write("D=M-D")

            # Skips the FALSE BLOCK if conditional is true.
            self._write(f"@START_TRUE_{self._con_index}")

            if "eq" == op:
                # if x - y == 0, then x == y.
                self._write("D;JEQ")
            elif "gt" == op:
                # if x - y > 0, then x > y.
                self._write("D;JGT")
            elif "lt" == op:
                # if x - y < 0, then x < y.
                self._write("D;JLT")

            ## START FALSE BLOCK ##
            self._write("@SP")
            self._write("A=M")
            self._write("M=0")

            # Skip to the end of the TRUE BLOCK.
            self._write(f"@END_TRUE_{self._con_index}")
            self._write("0;JMP")
            ## END FALSE BLOCK ##

            ## START TRUE BLOCK ##
            # Marks the start of the TRUE BLOCK.
            self._write(f"(START_TRUE_{self._con_index})")
            self._write("@SP")
            self._write("A=M")
            self._write("M=-1")

            # Marks the end of the TRUE BLOCK.
            self._write(f"(END_TRUE_{self._con_index})")
            ## END TRUE BLOCK ##

            self._con_index += 1
        else:
            raise Exception(f"Invalid op code: {op}")

        self._inc_SP()

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

    def close_file(self) -> None:
        """
        Closes the output file/stream.
        """
        self._out_file.close()

    def _write(self, cmd: str) -> None:
        self._out_file.write(f"{cmd}\n")

    def _goto_seg_addr(self, seg: str, offset_or_const: int) -> None:
        if "constant" == seg:
            self._write(f"@{offset_or_const}")

        elif "static" == seg:
            self._write(f"@{self._out_file.name}.{offset_or_const}")

        elif seg in MAPPED_SEGMENTS:
            if "pointer" == seg and (offset_or_const != 0 and offset_or_const != 1):
                raise Exception(
                    f"Invalid pointer offset: {offset_or_const}. Value must be 0 or 1."
                )
            if "temp" == seg and 7 < offset_or_const:
                raise Exception(
                    "Invalid temp offset: {offset_or_const}. Offset must be between 0 - 7 inclusive."
                )

            self._write(f"@{MAPPED_SEGMENTS[seg] + offset_or_const}")

        elif seg in SYMBOLIC_SEGMENTS:
            # go to address where segment's base index is kept
            self._write(f"@{SYMBOLIC_SEGMENTS[seg]}")
            # put the segment's base index in D-reg
            self._write("D=M")
            # load the offset into A-reg
            self._write(f"@{offset_or_const}")
            # go to the address of segment's base index + the offset
            self._write("A=D+A")

        else:
            raise Exception(f"Invalid segment: {seg}")

    def _inc_SP(self):
        # go to where stack pointer address is kept
        self._write("@SP")
        # increment the stack pointer's address value and go to new address
        self._write("AM=M+1")

    def _dec_SP(self) -> None:
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
        self._inc_SP()

    def _pop_to_D(self) -> None:
        self._dec_SP()
        # store the value at the stack pointer's address into D-reg
        self._write("D=M")
