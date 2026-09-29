"""Domain representation of whether membership months are already paid."""

from dataclasses import dataclass, field
from enum import Enum

from .start_position import StartPosition


class MonthState(Enum):
    """Payment state for a membership month."""

    EMPTY = "empty"
    PAID = "paid"


@dataclass
class MonthAvailability:
    """Track paid and empty month states independently of workbook storage."""

    states: dict[StartPosition, MonthState] = field(default_factory=dict)

    def state_for(self, position: StartPosition) -> MonthState:
        """Return the known state, treating an unrecorded month as empty."""
        return self.states.get(position, MonthState.EMPTY)

    def is_available(self, position: StartPosition) -> bool:
        """Return whether ``position`` is empty and can receive an allocation."""
        return self.state_for(position) is MonthState.EMPTY

    def set_state(self, position: StartPosition, state: MonthState) -> None:
        """Record the state of ``position``."""
        self.states[position] = state