"""Payment group domain entity."""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .customer import Customer


@dataclass
class PaymentGroup:
    """Represent a billing group shared by one or more customers."""

    name: str
    description: str = ""
    monthly_amount: Decimal = Decimal("0")
    currency: str = "EUR"
    customers: list[Customer] = field(default_factory=list)

    def add_customer(self, customer: Customer) -> None:
        """Attach a customer to the group."""
        if customer not in self.customers:
            self.customers.append(customer)
