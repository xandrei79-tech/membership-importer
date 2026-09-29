"""Domain model describing a proposed payment allocation."""

from dataclasses import dataclass
from decimal import Decimal

from .customer import Customer
from .payment import Payment


@dataclass
class AllocationPlan:
    """Store allocation details without applying or persisting them."""

    customer: Customer
    payment: Payment
    allocations: list[object]
    amount_allocated: Decimal
    amount_remaining: Decimal
    warnings: list[str]
    status: str