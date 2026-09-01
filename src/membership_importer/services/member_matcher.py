"""Member matching service boundary."""

from typing import Any

from ..models.payment import Payment


class MemberMatcher:
    """Match payments to members without changing payment data."""

    def match(self, payment: Payment) -> Any | None:
        """Return the member matched to ``payment``, or ``None``."""
        return None