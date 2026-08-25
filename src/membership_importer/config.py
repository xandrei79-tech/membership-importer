"""Application configuration interfaces and value objects."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Config:
    """Represent application configuration without loading or validating it."""

    settings_path: Path


class ConfigManager:
    """Define the contract for loading application configuration."""

    def load(self, path: Path) -> Config:
        """Load configuration from ``path``."""
        raise NotImplementedError("Configuration loading is not implemented yet")