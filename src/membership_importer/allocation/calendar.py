"""Calendar operations for membership allocation positions."""

from datetime import date

from ..models.start_position import StartPosition


class Calendar:
    """Convert dates to month positions and navigate across calendar years."""

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

    def first(self, value: date) -> StartPosition:
        """Return the month position for the month containing ``value``."""
        month_index = value.month - 1
        return StartPosition(
            year=value.year,
            month_index=month_index,
            month_name=self.MONTH_NAMES[month_index],
        )

    def next(self, position: StartPosition) -> StartPosition:
        """Return the following calendar month, advancing the year if needed."""
        self._validate(position)
        if position.month_index == len(self.MONTH_NAMES) - 1:
            return StartPosition(
                year=position.year + 1,
                month_index=0,
                month_name=self.MONTH_NAMES[0],
            )

        month_index = position.month_index + 1
        return StartPosition(
            year=position.year,
            month_index=month_index,
            month_name=self.MONTH_NAMES[month_index],
        )

    def previous(self, position: StartPosition) -> StartPosition:
        """Return the preceding calendar month, decrementing the year if needed."""
        self._validate(position)
        if position.month_index == 0:
            month_index = len(self.MONTH_NAMES) - 1
            return StartPosition(
                year=position.year - 1,
                month_index=month_index,
                month_name=self.MONTH_NAMES[month_index],
            )

        month_index = position.month_index - 1
        return StartPosition(
            year=position.year,
            month_index=month_index,
            month_name=self.MONTH_NAMES[month_index],
        )

    def _validate(self, position: StartPosition) -> None:
        if not 0 <= position.month_index < len(self.MONTH_NAMES):
            raise ValueError(f"Invalid month index: {position.month_index}")