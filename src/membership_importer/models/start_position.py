"""Value object identifying the first year and month for a payment."""

from dataclasses import dataclass


@dataclass(frozen=True)
class StartPosition:
    """Represent a worksheet year and zero-based month position."""

    year: int
    month_index: int
    month_name: str