from datetime import date

import pytest

from membership_importer.allocation.calendar import Calendar
from membership_importer.models.start_position import StartPosition


@pytest.mark.parametrize(
    ("input_date", "expected"),
    [
        (date(2026, 3, 18), StartPosition(2026, 2, "March")),
        (date(2026, 12, 1), StartPosition(2026, 11, "December")),
    ],
)
def test_first_returns_month_position(input_date: date, expected: StartPosition) -> None:
    assert Calendar().first(input_date) == expected


def test_next_advances_across_year_transition() -> None:
    december = StartPosition(2026, 11, "December")

    assert Calendar().next(december) == StartPosition(2027, 0, "January")


def test_previous_advances_back_across_year_transition() -> None:
    january = StartPosition(2027, 0, "January")

    assert Calendar().previous(january) == StartPosition(2026, 11, "December")


def test_next_and_previous_move_within_year() -> None:
    calendar = Calendar()
    march = StartPosition(2026, 2, "March")

    assert calendar.next(march) == StartPosition(2026, 3, "April")
    assert calendar.previous(march) == StartPosition(2026, 1, "February")


@pytest.mark.parametrize("operation", ["next", "previous"])
def test_navigation_rejects_invalid_month_index(operation: str) -> None:
    invalid = StartPosition(2026, 12, "December")

    with pytest.raises(ValueError, match="Invalid month index"):
        getattr(Calendar(), operation)(invalid)
