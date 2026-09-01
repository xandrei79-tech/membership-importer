"""Service boundary for the membership import workflow."""

from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from ..bank_importer import BankImporter
from ..excel.manager import ExcelManager, WorkbookAnalysisResult
from ..models.payment import Payment
from .member_matcher import MemberMatcher


@dataclass(frozen=True)
class ImportResult:
    """Store the workbook and payments collected for an import."""

    workbook_analysis: WorkbookAnalysisResult
    payments: list[Payment]


class ImportService:
    """Coordinate the future membership import workflow."""

    def __init__(self) -> None:
        self._excel_manager = ExcelManager()
        self._member_matcher = MemberMatcher()

    def analyze_workbook(self) -> None:
        raise NotImplementedError

    def import_payments(
        self,
        workbook_path: Path | str,
        bank_statement_paths: Sequence[Path | str],
    ) -> ImportResult:
        """Load the workbook and collect payments from each statement importer."""
        if not str(workbook_path).strip() or str(workbook_path) == ".":
            raise ValueError("Workbook path is required.")
        if not bank_statement_paths:
            raise ValueError("At least one bank statement path is required.")
        if any(not str(path).strip() for path in bank_statement_paths):
            raise ValueError("Bank statement paths must not be empty.")

        workbook_analysis = self.load_workbook(Path(workbook_path))
        payments: list[Payment] = []
        for path in bank_statement_paths:
            importer = self._detect_bank(Path(path))
            payments.extend(importer.import_statement(Path(path)))
        for payment in payments:
            self._member_matcher.match(payment)
        return ImportResult(
            workbook_analysis=workbook_analysis,
            payments=payments,
        )

    def _detect_bank(self, statement_path: Path) -> BankImporter:
        """Return the importer for ``statement_path`` when one is available."""
        raise NotImplementedError(
            f"No bank importer is implemented for '{statement_path.name}'."
        )

    def load_workbook(self, path: Path) -> WorkbookAnalysisResult:
        """Load a workbook through the existing Excel manager."""
        return self._excel_manager.load_workbook(path)