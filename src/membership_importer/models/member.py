"""Membership domain entity."""

from dataclasses import dataclass, field
from decimal import Decimal

from .payment import Payment


@dataclass
class Member:
    """Represent a membership record and its received payments."""

    mac: str
    full_name: str
    active: bool = True
    notes: str = ""
    payments: list[Payment] = field(default_factory=list)

    def add_payment(self, payment: Payment) -> None:
        """Add a payment to the member's payment history."""
        self.payments.append(payment)

    def total_paid(self) -> Decimal:
        """Return the total amount of the member's payments."""
        return sum((payment.amount for payment in self.payments), Decimal("0"))

    def has_payments(self) -> bool:
        """Return whether the member has received any payments."""
        return bool(self.payments)