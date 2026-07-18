"""Domain exceptions independent from transport and UI frameworks."""


class DgtError(Exception):
    """Base error for the application."""


class DgtDownloadError(DgtError):
    """Raised when a remote DGT resource cannot be downloaded."""


class DgtParseError(DgtError):
    """Raised when a DATEX2 document cannot be parsed."""


class DgtValidationError(DgtError):
    """Raised when input cannot satisfy a use-case contract."""