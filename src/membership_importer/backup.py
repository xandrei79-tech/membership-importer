"""Interfaces for creating safe workbook backups."""

from pathlib import Path


class BackupManager:
    """Define the contract for backup creation before an import."""

    def create_backup(self, source: Path, destination: Path) -> None:
        """Create a backup of ``source`` at ``destination``."""
        raise NotImplementedError("Backup creation is not implemented yet")