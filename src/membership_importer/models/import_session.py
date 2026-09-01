"""Import session domain entity."""

from dataclasses import dataclass, field
from decimal import Decimal

from .payment import Payment
from .workbook import Workbook


@dataclass
class ImportSession:
    """Track workbook and payment state for one import session."""

    workbook: Workbook | None = None
    payments: list[Payment] = field(default_factory=list)
    completed: bool = False

    def set_workbook(self, workbook: Workbook) -> None:
        """Set the workbook associated with the session."""
        self.workbook = workbook

    def add_payment(self, payment: Payment) -> None:
        """Add a payment to the session."""
        self.payments.append(payment)

    def total_paid(self) -> Decimal:
        """Return the total amount collected in the session."""
        return sum((payment.amount for payment in self.payments), Decimal("0"))

    def complete(self) -> None:
        """Mark the session as completed."""
        self.completed = True

    def is_complete(self) -> bool:
        """Return whether the session is completed."""
        return self.completed