"""Workbook structure analysis."""

from dataclasses import dataclass
import re
from typing import Any


@dataclass(frozen=True)
class WorkbookAnalysis:
    """Store the structural metadata detected in a workbook."""

    worksheet_names: tuple[str, ...]
    active_worksheet: str
    header_row: int | None
    first_data_row: int | None
    last_data_row: int | None
    detected_year: str | None
    month_columns: dict[str, int]
    mac_column: int | None


class WorkbookAnalyzer:
    """Analyze workbook structure without changing workbook contents."""

    MONTH_NAMES = {
        "january": "january",
        "jan": "january",
        "february": "february",
        "feb": "february",
        "march": "march",
        "mar": "march",
        "april": "april",
        "apr": "april",
        "may": "may",
        "june": "june",
        "jun": "june",
        "july": "july",
        "jul": "july",
        "august": "august",
        "aug": "august",
        "september": "september",
        "sep": "september",
        "sept": "september",
        "october": "october",
        "oct": "october",
        "november": "november",
        "nov": "november",
        "december": "december",
        "dec": "december",
    }

    def analyze(self, workbook: Any) -> WorkbookAnalysis:
        """Analyze the active worksheet in a loaded workbook."""
        worksheet_names = tuple(workbook.sheetnames)
        active_worksheet = workbook.active
        header_row, mac_column, month_columns = self._find_header(active_worksheet)
        first_data_row, last_data_row = self._find_data_bounds(
            active_worksheet,
            header_row,
        )
        detected_year = self._detect_year(active_worksheet.title, worksheet_names)
        return WorkbookAnalysis(
            worksheet_names=worksheet_names,
            active_worksheet=active_worksheet.title,
            header_row=header_row,
            first_data_row=first_data_row,
            last_data_row=last_data_row,
            detected_year=detected_year,
            month_columns=month_columns,
            mac_column=mac_column,
        )

    def _find_header(self, worksheet: Any) -> tuple[int | None, int | None, dict[str, int]]:
        for row in worksheet.iter_rows(min_row=1, max_row=min(worksheet.max_row, 100)):
            mac_column = None
            month_columns: dict[str, int] = {}
            for cell in row:
                value = self._normalize(cell.value)
                if value == "mac":
                    mac_column = cell.column
                if value in self.MONTH_NAMES:
                    month_columns[self.MONTH_NAMES[value]] = cell.column
            if mac_column is not None or month_columns:
                return row[0].row, mac_column, month_columns
        return None, None, {}

    def _find_data_bounds(
        self,
        worksheet: Any,
        header_row: int | None,
    ) -> tuple[int | None, int | None]:
        if header_row is None:
            return None, None
        data_rows = [
            row_number
            for row_number in range(header_row + 1, worksheet.max_row + 1)
            if any(
                cell.value is not None
                for cell in worksheet[row_number][: worksheet.max_column]
            )
        ]
        if not data_rows:
            return None, None
        return data_rows[0], data_rows[-1]

    def _detect_year(
        self,
        active_worksheet_name: str,
        worksheet_names: tuple[str, ...],
    ) -> str | None:
        active_year = re.search(r"\b(20\d{2})\b", active_worksheet_name)
        if active_year:
            return active_year.group(1)
        years = [
            match.group(1)
            for worksheet_name in worksheet_names
            if (match := re.search(r"\b(20\d{2})\b", worksheet_name))
        ]
        return years[0] if len(years) == 1 else None

    @staticmethod
    def _normalize(value: Any) -> str:
        return "" if value is None else str(value).strip().lower()
