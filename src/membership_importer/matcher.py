"""Interfaces for matching bank payments to membership records."""

from typing import Any


class Matcher:
    """Define the contract for payment matching."""

    def match(self, payment: Any, member: Any) -> bool:
        """Determine whether ``payment`` belongs to ``member``."""
        raise NotImplementedError("Payment matching is not implemented yet")