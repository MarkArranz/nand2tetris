from os import path

from asm_writer import CodeWriter
from constants import CommandType
from vm_parser import Parser


def main(vm_file: str) -> None:
    root, ext = path.splitext(vm_file)

    if ".vm" != ext:
        raise NotImplementedError(
            f"Cannot read {ext} files. Only .vm files are allowed."
        )

    output_file = f"{root}.asm"
    pr = Parser(vm_file)
    cw = CodeWriter(output_file)

    print(f"Translating {vm_file}...")

    try:
        while pr.has_more_lines:
            pr.advance()
            cw.write_comment(pr.cur_instr)

            if CommandType.C_ARITHMETIC == pr.command_type:
                cw.write_arithmetic(pr.arg1, pr.arg2)
            else:
                cw.write_push_pop(pr.command_type, pr.arg1, pr.arg2)
    finally:
        pr.close()
        cw.close()

    print(f"Successfully translated {vm_file} to {output_file}")


if "__main__" == __name__:
    import sys

    vm_file = sys.argv[1]
    main(vm_file)
