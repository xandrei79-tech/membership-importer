"""Interfaces for importing bank statement data."""

from pathlib import Path

from .models.payment import Payment


class BankImporter:
    """Define the contract for bank statement importers."""

    def import_statement(self, path: Path) -> list[Payment]:
        """Import a bank statement from ``path``."""
        raise NotImplementedError("Bank statement importing is not implemented yet")