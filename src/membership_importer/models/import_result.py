"""Import result domain entity."""

from dataclasses import dataclass, field
from decimal import Decimal

from .payment import Payment
from .workbook import Workbook


@dataclass
class ImportResult:
    """Represent the domain data collected during an import."""

    workbook: Workbook
    payments: list[Payment] = field(default_factory=list)

    def add_payment(self, payment: Payment) -> None:
        """Add a payment to the import result."""
        self.payments.append(payment)

    def total_paid(self) -> Decimal:
        """Return the total amount in the import result."""
        return sum((payment.amount for payment in self.payments), Decimal("0"))

    def has_payments(self) -> bool:
        """Return whether the import result contains payments."""
        return bool(self.payments)