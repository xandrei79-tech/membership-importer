from pathlib import Path

from membership_importer.models.workbook import Workbook


def test_workbook_queries_worksheet_metadata() -> None:
    workbook = Workbook(
        path=Path("membership.xlsx"),
        worksheet_names=("2025", "2026"),
        active_worksheet_name="2025",
    )

    assert workbook.is_loaded() is True
    assert workbook.has_worksheet("2025") is True
    assert workbook.has_worksheet("2027") is False
    assert workbook.has_worksheets(("2025", "2026")) is True
    assert workbook.has_worksheets(("2025", "2027")) is False


def test_empty_workbook_is_not_loaded() -> None:
    workbook = Workbook(path=Path("membership.xlsx"))

    assert workbook.is_loaded() is False
    assert workbook.has_worksheets(()) is True
