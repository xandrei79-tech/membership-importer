"""Customer domain entity."""

from __future__ import annotations

from dataclasses import dataclass, field

from .member import Member
from .payment_group import PaymentGroup


@dataclass
class Customer:
    """Represent a customer and the members attached to that customer."""

    customer_id: str
    customer_name: str
    group: PaymentGroup | None = None
    members: list[Member] = field(default_factory=list)

    def add_member(self, member: Member) -> None:
        """Attach a member to the customer."""
        if member not in self.members:
            self.members.append(member)
