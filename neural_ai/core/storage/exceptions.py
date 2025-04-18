"""Storage komponens kivételek."""

from typing import Optional


class StorageError(Exception):
    """Alap kivétel a storage műveletekhez."""

    def __init__(self, message: str, original_error: Optional[Exception] = None) -> None:
        """Kivétel inicializálása.

        Args:
            message: Hibaüzenet
            original_error: Eredeti kivétel, ha van
        """
        super().__init__(message)
        self.original_error = original_error


class StorageFormatError(StorageError):
    """Nem támogatott vagy érvénytelen formátum esetén."""


class StorageSerializationError(StorageError):
    """Szerializációs vagy deszerializációs hiba esetén."""


class StorageIOError(StorageError):
    """I/O műveletek során fellépő hibák esetén."""


class StoragePermissionError(StorageError):
    """Jogosultsági hibák esetén."""


class StorageNotFoundError(StorageError):
    """Nem létező erőforrás esetén."""


class StorageValidationError(StorageError):
    """Érvénytelen adat vagy paraméter esetén."""
