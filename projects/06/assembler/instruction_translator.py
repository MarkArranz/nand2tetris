from hack_constants import COMP_CODES, JUMP_CODES


class Translator:
    @staticmethod
    def comp(instr: str) -> str:
        return COMP_CODES[instr]

    @staticmethod
    def dest(instr: str) -> str:
        """
        Constructs a binary string by flipping the corresponding letter's
        positional bit to 1 if the instruction string contains the letter:

        Letter   || A | D | M
        Bit Pos. || 0 | 0 | 0

        """
        dest_bits = 0b_000

        for c in instr:
            match c:
                case "A":
                    # Flip the 4 bit: 000 => 100
                    dest_bits |= 1 << 2
                case "D":
                    # Flip the 2 bit: 000 => 010
                    dest_bits |= 1 << 1
                case "M":
                    # Flip the 0 bit: 000 => 001
                    dest_bits |= 1 << 0
                case _:
                    pass

        return format(dest_bits, "03b")

    @staticmethod
    def jump(instr: str) -> str:
        return JUMP_CODES[instr]

    @staticmethod
    def instruction(instr: int) -> str:
        return format(instr, "016b")
