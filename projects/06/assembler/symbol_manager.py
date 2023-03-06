from logging import getLogger
from typing import Dict

from hack_constants import PREDEFINED_SYMBOLS, VAR_SYMBOL_START_ADDR

logger = getLogger(__name__)


class SymbolManager:
    def __init__(self) -> None:
        self._next_var_addr = VAR_SYMBOL_START_ADDR
        self._symbol_table: Dict[str, int] = {}

    def add_entry(self, symbol: str, address: int) -> None:
        """Adds `<symbol,address>` to the symbols table."""
        if 0 > address:
            raise SyntaxError("Address cannot be negative.")

        if self._symbol_table.get(symbol) == address:
            logger.warn(f"({symbol}, {address}) already exists in symbol table")
            return None

        self._symbol_table[symbol] = address

    def contains(self, symbol: str) -> bool:
        """Does the symbol table contain the given `symbol`?"""
        return symbol in self._symbol_table

    def get_address(self, symbol: str) -> int:
        """Returns the address associated with the `symbol`."""
        return self._symbol_table[symbol]

    def assign_address(self, symbol: str) -> None:
        """Assigns the next variable address to the given symbol."""
        if self.contains(symbol):
            logger.warn(
                f"({symbol}, {self.get_address(symbol)}) already exists in symbol table"
            )
            return None

        if symbol in PREDEFINED_SYMBOLS:
            self.add_entry(symbol, PREDEFINED_SYMBOLS[symbol])
            return None

        self.add_entry(symbol, self._next_var_addr)
        self._next_var_addr += 1
        return None
