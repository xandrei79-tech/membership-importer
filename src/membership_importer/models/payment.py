"""Unified payment data model."""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Any


@dataclass
class Payment:
    """Represent a payment independently of its source bank."""

    payment_date: date
    amount: Decimal
    payer_name: str
    description: str
    reference_number: str | None
    source_bank: str
    original_record: Any

    def has_reference_number(self) -> bool:
        """Return whether the payment includes a reference number."""
        return bool(self.reference_number)

    def is_from_bank(self, bank_name: str) -> bool:
        """Return whether the payment came from ``bank_name``."""
        return self.source_bank == bank_name