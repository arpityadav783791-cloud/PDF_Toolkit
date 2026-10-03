from app.exceptions.base import PdfToolkitError


class FileError(PdfToolkitError):
    """Base file operation error."""


class FileNotFoundError(FileError):
    """Raised when a required file does not exist."""


class FilePermissionError(FileError):
    """Raised when a file cannot be accessed."""
