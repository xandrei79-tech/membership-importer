from pathlib import Path

import pytest

from membership_importer.allocation.rules.year_transition_rule import YearTransitionRule
from membership_importer.exceptions import WorksheetNotFound
from membership_importer.models.start_position import StartPosition
from membership_importer.models.workbook import Workbook


def test_year_transition_rule_advances_december_to_next_january() -> None:
    december = StartPosition(year=2026, month_index=11, month_name="December")
    workbook = Workbook(path=Path("membership.xlsx"), worksheet_names=("2026", "2027"))

    assert YearTransitionRule().determine(december, workbook) == StartPosition(
        year=2027,
        month_index=0,
        month_name="January",
    )


def test_year_transition_rule_raises_when_target_worksheet_is_missing() -> None:
    december = StartPosition(year=2026, month_index=11, month_name="December")
    workbook = Workbook(path=Path("membership.xlsx"), worksheet_names=("2026",))

    with pytest.raises(WorksheetNotFound):
        YearTransitionRule().determine(december, workbook)