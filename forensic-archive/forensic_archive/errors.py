"""Fail-closed errors for museum-grade packaging."""


class MuseumPackageError(ValueError):
    """Raised when a run cannot produce a trustworthy archive."""


class MuseumIntegrityError(ValueError):
    """Raised when an existing package fails verification."""
