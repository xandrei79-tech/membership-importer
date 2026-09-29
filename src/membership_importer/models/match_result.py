"""Result returned when matching a payment to a customer."""

from dataclasses import dataclass
from typing import Literal

from .customer import Customer

MatchStatus = Literal["matched", "unmatched", "ambiguous"]


@dataclass(frozen=True)
class MatchResult:
    """Describe the customer matching outcome without changing the payment."""

    status: MatchStatus
    customer: Customer | None = None
    candidates: tuple[Customer, ...] = ()