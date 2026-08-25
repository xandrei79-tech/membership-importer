"""Interfaces for reading and writing membership workbooks."""

from pathlib import Path


class ExcelManager:
    """Coordinate workbook access while preserving the domain boundary."""

    def open_workbook(self, path: Path) -> None:
        """Open a membership workbook from ``path``."""
        raise NotImplementedError("Workbook management is not implemented yet")

    def save_workbook(self, path: Path) -> None:
        """Save the current workbook to ``path``."""
        raise NotImplementedError("Workbook management is not implemented yet")