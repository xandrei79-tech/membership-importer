"""Application entry point for Membership Importer."""

from .gui import Application


def main() -> None:
    """Create and start the application."""
    Application().run()


if __name__ == "__main__":
    main()
