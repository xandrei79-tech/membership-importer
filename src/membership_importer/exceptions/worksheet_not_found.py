"""Exception raised when a required workbook worksheet is unavailable."""


class WorksheetNotFound(Exception):
    """Signal that a required year worksheet does not exist in the workbook."""