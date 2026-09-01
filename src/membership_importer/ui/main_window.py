"""Presentation-layer entry points for the Membership Importer application."""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

from ..excel.manager import WorkbookAnalysisResult
from ..services.import_service import ImportService


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
        self.import_service = ImportService()
        self.workbook_analysis: WorkbookAnalysisResult | None = None

    def _configure_window(self) -> None:
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_GEOMETRY)
        self.root.update_idletasks()

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

        content = ttk.Frame(self.workspace, padding=20)
        content.pack(fill=tk.BOTH, expand=True)

        self._create_file_section(
            content,
            "Excel workbook",
            "workbook_path",
            row=0,
            browse_command=self._browse_workbook,
        )
        self._create_file_section(
            content,
            "Bank statement(s)",
            "bank_statements_path",
            row=1,
            browse_command=self._browse_bank_statements,
        )

        self.import_button = ttk.Button(
            content,
            text="Import",
            command=self._load_workbook,
            state=tk.DISABLED,
            width=20,
        )
        self.import_button.grid(row=2, column=0, columnspan=3, pady=(30, 0))
        self.bank_statement_paths: tuple[str, ...] = ()

        content.columnconfigure(1, weight=1)

    def _create_file_section(
        self,
        parent: ttk.Frame,
        label_text: str,
        variable_name: str,
        row: int,
        browse_command: object | None = None,
    ) -> None:
        variable = tk.StringVar()
        setattr(self, variable_name, variable)

        ttk.Label(parent, text=label_text).grid(
            row=row,
            column=0,
            padx=(0, 10),
            pady=5,
            sticky=tk.W,
        )
        ttk.Entry(
            parent,
            textvariable=variable,
            state="readonly",
        ).grid(row=row, column=1, padx=(0, 10), pady=5, sticky=tk.EW)
        ttk.Button(parent, text="Browse", command=browse_command).grid(
            row=row,
            column=2,
            pady=5,
        )

    def _browse_workbook(self) -> None:
        selected_path = filedialog.askopenfilename(
            parent=self.root,
            title="Select Excel workbook",
            filetypes=[
                ("Excel workbooks", ("*.xlsx", "*.xlsm")),
            ],
        )
        if selected_path:
            self.workbook_path.set(selected_path)
            self.import_button.configure(state=tk.NORMAL)

    def _load_workbook(self) -> None:
        workbook_path = self.workbook_path.get()
        bank_statement_paths = self.bank_statement_paths

        try:
            import_result = self.import_service.import_payments(
                workbook_path,
                bank_statement_paths,
            )
        except Exception as error:
            messagebox.showerror(
                "Import Error",
                str(error),
                parent=self.root,
            )
            return

        self.workbook_analysis = import_result.workbook_analysis
        messagebox.showinfo(
            "Workbook Loaded",
            "Workbook loaded successfully.",
            parent=self.root,
        )
        self._show_workbook_analysis(self.workbook_analysis)

    def _show_workbook_analysis(self, analysis: WorkbookAnalysisResult) -> None:
        worksheet_lines = "\n".join(
            f"- {worksheet_name}" for worksheet_name in analysis.worksheet_names
        )
        found_lines = "\n".join(
            f"{year} {chr(0x2714) if found else chr(0x2718)}"
            for year, found in analysis.required_worksheets.items()
        )

        analysis_message = (
            "Worksheets:\n"
            f"{worksheet_lines}\n\n"
            "Active worksheet:\n"
            f"{analysis.active_worksheet_name}\n\n"
            "Found:\n"
            f"{found_lines}"
        )
        messagebox.showinfo(
            "Workbook analysis",
            analysis_message,
            parent=self.root,
        )

    def _browse_bank_statements(self) -> None:
        selected_paths = filedialog.askopenfilenames(
            parent=self.root,
            title="Select bank statement(s)",
            filetypes=[
                ("Bank statements", ("*.pdf", "*.csv", "*.xlsx", "*.xls")),
            ],
        )
        if selected_paths:
            self.bank_statement_paths = tuple(selected_paths)
            filenames = [Path(path).name for path in selected_paths]
            self.bank_statements_path.set(", ".join(filenames))

    def _create_status_bar(self) -> None:
        self.status_bar = ttk.Frame(self.root)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def run(self) -> None:
        """Start the application event loop."""
        self.root.mainloop()