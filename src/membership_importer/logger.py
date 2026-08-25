"""Interfaces for recording membership import activity."""

from typing import Any


class ImportLogger:
    """Define the contract for import event logging."""

    def log(self, event: Any) -> None:
        """Record an import ``event``."""
        raise NotImplementedError("Import logging is not implemented yet")