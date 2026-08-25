"""Interfaces for importing bank statement data."""

from pathlib import Path


class BankImporter:
    """Define the contract for bank statement importers."""

    def import_statement(self, path: Path) -> None:
        """Import a bank statement from ``path``."""
        raise NotImplementedError("Bank statement importing is not implemented yet")