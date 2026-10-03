from app.exceptions.base import PdfToolkitError


class PdfError(PdfToolkitError):
    """Base PDF processing error."""


class InvalidPdfError(PdfError):
    """Raised when a PDF is invalid or unreadable."""


class EncryptedPdfError(PdfError):
    """Raised when a PDF requires authentication."""


class PdfValidationError(PdfError):
    """Raised when a generated PDF fails validation."""
