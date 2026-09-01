"""Workbook domain entity."""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Workbook:
    """Represent workbook identity and inspected worksheet metadata."""

    path: Path
    worksheet_names: tuple[str, ...] = ()
    active_worksheet_name: str | None = None

    def has_worksheet(self, worksheet_name: str) -> bool:
        """Return whether the workbook contains ``worksheet_name``."""
        return worksheet_name in self.worksheet_names

    def has_worksheets(self, worksheet_names: tuple[str, ...]) -> bool:
        """Return whether the workbook contains every named worksheet."""
        return all(self.has_worksheet(name) for name in worksheet_names)

    def is_loaded(self) -> bool:
        """Return whether worksheet metadata has been loaded."""
        return bool(self.worksheet_names)