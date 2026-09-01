import tkinter as tk

import pytest

from membership_importer.ui.main_window import (
    WINDOW_GEOMETRY,
    WINDOW_TITLE,
    Application,
)


@pytest.fixture
def application() -> Application:
    try:
        root = tk.Tk()
    except tk.TclError as error:
        pytest.skip(f"Tk display is unavailable: {error}")

    app = Application(root)
    yield app
    root.destroy()


def test_application_builds_empty_window(application: Application) -> None:
    assert application.root.title() == WINDOW_TITLE
    assert application.root.geometry().startswith(WINDOW_GEOMETRY)
    assert application.root.cget("menu") == str(application.menu_bar)
    assert application.toolbar.winfo_manager() == "pack"
    assert application.workspace.winfo_manager() == "pack"
    assert application.status_bar.winfo_manager() == "pack"
    assert application.toolbar.winfo_children() == []
    assert application.workspace.winfo_children() == []