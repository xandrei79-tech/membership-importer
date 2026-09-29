"""Advance a December start position to January of the next worksheet year."""

from ...exceptions import WorksheetNotFound
from ...models.start_position import StartPosition
from ...models.workbook import Workbook


class YearTransitionRule:
    """Transition from December to January when the next year is available."""

    def determine(self, position: StartPosition, workbook: Workbook) -> StartPosition:
        """Return next year's January position, or fail if its worksheet is absent."""
        if position.month_index != 11:
            raise ValueError("Year transition is only valid from December.")

        next_year = position.year + 1
        if not workbook.has_worksheet(str(next_year)):
            raise WorksheetNotFound(
                f"Worksheet for year {next_year} was not found."
            )

        return StartPosition(
            year=next_year,
            month_index=0,
            month_name="January",
        )