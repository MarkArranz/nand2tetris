import logging
import pdb
import sys
from os import path

from asm_parser import AsmParser
from hack_types import InstructionType, LineType
from instruction_translator import Translator
from symbol_manager import SymbolManager

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)


def assemble_binary_file(asm_file: str) -> None:

    root, ext = path.splitext(asm_file)
    if ".asm" != ext:
        raise NotImplementedError(
            f"Cannot read {ext} files. Only .asm files are allowed."
        )

    output_file = f"{root}.hack"
    with open(asm_file) as symbolic_asm_file, open(output_file, "w") as binary_asm_file:

        symbol_mgr = SymbolManager()
        parser = AsmParser()
        output_line_number = 0

        # FIRST PASS: Build symbol table
        for lineno, line in enumerate(symbolic_asm_file, 1):
            # Skip blank lines and comments
            text = content[0] if (content := line.split()) else None
            if not text or text.startswith("//"):
                continue

            try:
                parser.parse(text)
            except SyntaxError as err:
                err.filename = asm_file
                err.lineno = lineno
                err.text = line
                raise

            if parser.line_type == LineType.LABEL_DECLARATION:
                symbol_mgr.add_entry(text.strip("()"), output_line_number)
            else:
                # Increment goto_lineno by 1 whenever an assembly instruction is encountered.
                output_line_number += 1

        # SECOND PASS: Generate binary code
        symbolic_asm_file.seek(0)  # Begin reading at the start of the file again.
        for lineno, line in enumerate(symbolic_asm_file, 1):
            # Skip blank lines and comments
            text = content[0] if (content := line.split()) else None
            if not text or text.startswith("//"):
                continue

            try:
                parser.parse(text)
            except SyntaxError as err:
                err.filename = asm_file
                err.lineno = lineno
                err.text = line
                raise

            # Skip label declarations
            if parser.line_type == LineType.LABEL_DECLARATION:
                continue

            try:
                # Based on the InstructionType, translate the symbolic assembly code to binary assembly.
                match parser.instruction_type:
                    case InstructionType.NUMERIC_A:
                        binary_asm_file.write(
                            f"{Translator.instruction(int(parser.instruction))}\n"
                        )
                    case InstructionType.SYMBOLIC_A:
                        if not symbol_mgr.contains(parser.instruction):
                            symbol_mgr.assign_address(parser.instruction)

                        addr = symbol_mgr.get_address(parser.instruction)
                        binary_asm_file.write(f"{Translator.instruction(addr)}\n")
                    case InstructionType.SYMBOLIC_C:
                        comp = Translator.comp(parser.comp)
                        dest = Translator.dest(parser.dest)
                        jump = Translator.jump(parser.jump)
                        binary_asm_file.write(f"111{comp}{dest}{jump}\n")
                    case _:
                        pass
            except:
                logger.debug(vars(parser))
                raise

    logger.info(f"...assembling {asm_file} to {output_file} FINISHED!")


if __name__ == "__main__":
    asm_files = sys.argv[1:]

    if not asm_files:
        raise FileNotFoundError("No file provided.")

    for asm_file in asm_files:
        logger.info(f"Assembling {asm_file}...")
        try:
            assemble_binary_file(asm_file)
        except Exception as e:
            logger.exception(e)
            logger.warn(f"Skipping {asm_file}")
            continue
