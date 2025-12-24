"""Tesztek a neural_ai.core.storage.exceptions modulhoz."""

from neural_ai.core.storage.exceptions import (
    StorageError,
    StorageFormatError,
    StorageIOError,
    StorageNotFoundError,
    StorageSerializationError,
    StorageValidationError,
)


class TestStorageError:
    """StorageError osztály tesztjei."""

    def test_initialization_with_message(self) -> None:
        """Teszteli a kivétel inicializálását csak üzenettel."""
        message = "Teszt hibaüzenet"
        error = StorageError(message)

        assert str(error) == message
        assert error.original_error is None

    def test_initialization_with_original_error(self) -> None:
        """Teszteli a kivétel inicializálását üzenettel és eredeti hibával."""
        message = "Csomagoló hibaüzenet"
        original = ValueError("Eredeti hiba")

        error = StorageError(message, original)

        assert str(error) == message
        assert error.original_error is original
        assert isinstance(error.original_error, ValueError)


class TestStorageFormatError:
    """StorageFormatError osztály tesztjei."""

    def test_is_instance_of_storage_error(self) -> None:
        """Teszteli, hogy a StorageFormatError a StorageError leszármazottja."""
        error = StorageFormatError("Formátum hiba")
        assert isinstance(error, StorageError)


class TestStorageSerializationError:
    """StorageSerializationError osztály tesztjei."""

    def test_is_instance_of_storage_error(self) -> None:
        """Teszteli, hogy a StorageSerializationError a StorageError leszármazottja."""
        error = StorageSerializationError("Szerializációs hiba")
        assert isinstance(error, StorageError)


class TestStorageIOError:
    """StorageIOError osztály tesztjei."""

    def test_is_instance_of_storage_error(self) -> None:
        """Teszteli, hogy a StorageIOError a StorageError leszármazottja."""
        error = StorageIOError("I/O hiba")
        assert isinstance(error, StorageError)


class TestStorageNotFoundError:
    """StorageNotFoundError osztály tesztjei."""

    def test_is_instance_of_storage_error(self) -> None:
        """Teszteli, hogy a StorageNotFoundError a StorageError leszármazottja."""
        error = StorageNotFoundError("Nem található hiba")
        assert isinstance(error, StorageError)


class TestStorageValidationError:
    """StorageValidationError osztály tesztjei."""

    def test_is_instance_of_storage_error(self) -> None:
        """Teszteli, hogy a StorageValidationError a StorageError leszármazottja."""
        error = StorageValidationError("Validációs hiba")
        assert isinstance(error, StorageError)
