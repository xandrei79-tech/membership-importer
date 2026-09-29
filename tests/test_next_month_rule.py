import pytest

from membership_importer.allocation.rules.next_month_rule import (
    NextMonthRule,
)
from membership_importer.models.start_position import StartPosition
from membership_importer.models.year_transition_required import YearTransitionRequired


@pytest.mark.parametrize(
    ("current", "expected"),
    [
        (
            StartPosition(year=2026, month_index=2, month_name="March"),
            StartPosition(year=2026, month_index=3, month_name="April"),
        ),
        (
            StartPosition(year=2026, month_index=10, month_name="November"),
            StartPosition(year=2026, month_index=11, month_name="December"),
        ),
    ],
)
def test_next_month_rule_advances_within_the_year(
    current: StartPosition,
    expected: StartPosition,
) -> None:
    assert NextMonthRule().determine(current) == expected


def test_next_month_rule_raises_when_current_month_is_december() -> None:
    december = StartPosition(year=2026, month_index=11, month_name="December")

    with pytest.raises(YearTransitionRequired):
        NextMonthRule().determine(december)
