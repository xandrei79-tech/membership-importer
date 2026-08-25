"""Presentation-layer entry points for the Membership Importer application."""

import tkinter as tk
from tkinter import ttk


WINDOW_TITLE = "Membership Importer"
WINDOW_GEOMETRY = "1000x700"


class Application:
    """Represent the desktop application lifecycle."""

    def __init__(self, root: tk.Tk | None = None) -> None:
        """Create the application window and its structural regions."""
        self.root = root or tk.Tk()
        self._configure_window()
        self._create_menu_bar()
        self._create_toolbar()
        self._create_workspace()
        self._create_status_bar()

    def _configure_window(self) -> None:
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_GEOMETRY)

    def _create_menu_bar(self) -> None:
        menu_bar = tk.Menu(self.root)
        self.root.configure(menu=menu_bar)
        self.menu_bar = menu_bar

    def _create_toolbar(self) -> None:
        self.toolbar = ttk.Frame(self.root)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

    def _create_workspace(self) -> None:
        self.workspace = ttk.Frame(self.root)
        self.workspace.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def _create_status_bar(self) -> None:
        self.status_bar = ttk.Frame(self.root)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def run(self) -> None:
        """Start the application event loop."""
        self.root.mainloop()