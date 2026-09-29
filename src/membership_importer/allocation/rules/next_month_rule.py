"""Advance a start position by one month without crossing a year boundary."""

from ...models.start_position import StartPosition
from ...models.year_transition_required import YearTransitionRequired


class NextMonthRule:
    """Return the next calendar month within the current year."""

    MONTH_NAMES = (
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    )

    def determine(self, position: StartPosition) -> StartPosition:
        """Return the month after ``position``, or raise at December."""
        if not 0 <= position.month_index < len(self.MONTH_NAMES):
            raise ValueError(f"Invalid month index: {position.month_index}")
        if position.month_index == len(self.MONTH_NAMES) - 1:
            raise YearTransitionRequired(
                "Advancing from December requires a worksheet year transition."
            )

        next_month_index = position.month_index + 1
        return StartPosition(
            year=position.year,
            month_index=next_month_index,
            month_name=self.MONTH_NAMES[next_month_index],
        )