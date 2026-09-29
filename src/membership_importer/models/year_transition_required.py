"""Exception raised when a month rule would cross into a new year."""


class YearTransitionRequired(Exception):
    """Signal that advancing from December requires separate year handling."""
