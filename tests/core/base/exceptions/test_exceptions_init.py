"""Core base exceptions modul __init__.py tesztelése.

Ez a modul teszteli a neural_ai.core.base.exceptions.__init__.py fájlban
definiált exportokat és funkcionalitásokat.
"""

from neural_ai.core.base.exceptions import (
    ComponentNotFoundError,
    ConfigurationError,
    ConnectionError,
    DependencyError,
    InsufficientDiskSpaceError,
    NetworkException,
    NeuralAIException,
    PermissionDeniedError,
    SingletonViolationError,
    StorageException,
    StoragePermissionError,
    StorageReadError,
    StorageWriteError,
    TimeoutError,
)


class TestExceptionsInit:
    """Exceptions modul __init__.py tesztjei."""

    def test_neural_ai_exception_import(self) -> None:
        """Teszteli, hogy a NeuralAIException importálható-e."""
        assert NeuralAIException is not None
        assert hasattr(NeuralAIException, "__name__")
        assert NeuralAIException.__name__ == "NeuralAIException"

    def test_storage_exception_import(self) -> None:
        """Teszteli, hogy a StorageException importálható-e."""
        assert StorageException is not None
        assert hasattr(StorageException, "__name__")
        assert StorageException.__name__ == "StorageException"

    def test_storage_write_error_import(self) -> None:
        """Teszteli, hogy a StorageWriteError importálható-e."""
        assert StorageWriteError is not None
        assert hasattr(StorageWriteError, "__name__")
        assert StorageWriteError.__name__ == "StorageWriteError"

    def test_storage_read_error_import(self) -> None:
        """Teszteli, hogy a StorageReadError importálható-e."""
        assert StorageReadError is not None
        assert hasattr(StorageReadError, "__name__")
        assert StorageReadError.__name__ == "StorageReadError"

    def test_storage_permission_error_import(self) -> None:
        """Teszteli, hogy a StoragePermissionError importálható-e."""
        assert StoragePermissionError is not None
        assert hasattr(StoragePermissionError, "__name__")
        assert StoragePermissionError.__name__ == "StoragePermissionError"

    def test_configuration_error_import(self) -> None:
        """Teszteli, hogy a ConfigurationError importálható-e."""
        assert ConfigurationError is not None
        assert hasattr(ConfigurationError, "__name__")
        assert ConfigurationError.__name__ == "ConfigurationError"

    def test_dependency_error_import(self) -> None:
        """Teszteli, hogy a DependencyError importálható-e."""
        assert DependencyError is not None
        assert hasattr(DependencyError, "__name__")
        assert DependencyError.__name__ == "DependencyError"

    def test_singleton_violation_error_import(self) -> None:
        """Teszteli, hogy a SingletonViolationError importálható-e."""
        assert SingletonViolationError is not None
        assert hasattr(SingletonViolationError, "__name__")
        assert SingletonViolationError.__name__ == "SingletonViolationError"

    def test_component_not_found_error_import(self) -> None:
        """Teszteli, hogy a ComponentNotFoundError importálható-e."""
        assert ComponentNotFoundError is not None
        assert hasattr(ComponentNotFoundError, "__name__")
        assert ComponentNotFoundError.__name__ == "ComponentNotFoundError"

    def test_network_exception_import(self) -> None:
        """Teszteli, hogy a NetworkException importálható-e."""
        assert NetworkException is not None
        assert hasattr(NetworkException, "__name__")
        assert NetworkException.__name__ == "NetworkException"

    def test_timeout_error_import(self) -> None:
        """Teszteli, hogy a TimeoutError importálható-e."""
        assert TimeoutError is not None
        assert hasattr(TimeoutError, "__name__")
        assert TimeoutError.__name__ == "TimeoutError"

    def test_connection_error_import(self) -> None:
        """Teszteli, hogy a ConnectionError importálható-e."""
        assert ConnectionError is not None
        assert hasattr(ConnectionError, "__name__")
        assert ConnectionError.__name__ == "ConnectionError"

    def test_insufficient_disk_space_error_import(self) -> None:
        """Teszteli, hogy a InsufficientDiskSpaceError importálható-e."""
        assert InsufficientDiskSpaceError is not None
        assert hasattr(InsufficientDiskSpaceError, "__name__")
        assert InsufficientDiskSpaceError.__name__ == "InsufficientDiskSpaceError"

    def test_permission_denied_error_import(self) -> None:
        """Teszteli, hogy a PermissionDeniedError importálható-e."""
        assert PermissionDeniedError is not None
        assert hasattr(PermissionDeniedError, "__name__")
        assert PermissionDeniedError.__name__ == "PermissionDeniedError"

    def test_all_exports_available(self) -> None:
        """Teszteli, hogy minden exportált kivétel elérhető-e."""
        from neural_ai.core.base.exceptions import __all__

        expected_exports = [
            "NeuralAIException",
            "StorageException",
            "StorageWriteError",
            "StorageReadError",
            "StoragePermissionError",
            "ConfigurationError",
            "DependencyError",
            "SingletonViolationError",
            "ComponentNotFoundError",
            "NetworkException",
            "TimeoutError",
            "ConnectionError",
            "InsufficientDiskSpaceError",
            "PermissionDeniedError",
        ]
        assert __all__ == expected_exports

        # Minden exportált kivétel importálható
        for export_name in __all__:
            module = __import__("neural_ai.core.base.exceptions", fromlist=[export_name])
            export_exception = getattr(module, export_name)
            assert export_exception is not None

    def test_exception_inheritance_hierarchy(self) -> None:
        """Teszteli a kivételek öröklődési hierarchiáját."""
        # NeuralAIException az alap kivétel
        assert issubclass(StorageException, NeuralAIException)
        assert issubclass(ConfigurationError, NeuralAIException)
        assert issubclass(DependencyError, NeuralAIException)
        assert issubclass(SingletonViolationError, NeuralAIException)
        assert issubclass(ComponentNotFoundError, NeuralAIException)
        assert issubclass(NetworkException, NeuralAIException)

        # StorageException leszármazottjai
        assert issubclass(StorageWriteError, StorageException)
        assert issubclass(StorageReadError, StorageException)
        assert issubclass(StoragePermissionError, StorageException)
        assert issubclass(InsufficientDiskSpaceError, StorageException)
        assert issubclass(PermissionDeniedError, StorageException)

        # NetworkException leszármazottjai
        assert issubclass(TimeoutError, NetworkException)
        assert issubclass(ConnectionError, NetworkException)

    def test_exceptions_can_be_raised(self) -> None:
        """Teszteli, hogy a kivételek dobhatók-e."""
        import pytest

        # NeuralAIException
        with pytest.raises(NeuralAIException):
            raise NeuralAIException("Teszt hiba")

        # StorageException
        with pytest.raises(StorageException):
            raise StorageException("Tárolási hiba")

        # ConfigurationError
        with pytest.raises(ConfigurationError):
            raise ConfigurationError("Konfigurációs hiba")

        # DependencyError
        with pytest.raises(DependencyError):
            raise DependencyError("Függőségi hiba")

        # SingletonViolationError
        with pytest.raises(SingletonViolationError):
            raise SingletonViolationError("Singleton megsértése")

        # ComponentNotFoundError
        with pytest.raises(ComponentNotFoundError):
            raise ComponentNotFoundError("Komponens nem található")

        # NetworkException
        with pytest.raises(NetworkException):
            raise NetworkException("Hálózati hiba")

        # StorageWriteError
        with pytest.raises(StorageWriteError):
            raise StorageWriteError("Írási hiba")

        # StorageReadError
        with pytest.raises(StorageReadError):
            raise StorageReadError("Olvasási hiba")

        # StoragePermissionError
        with pytest.raises(StoragePermissionError):
            raise StoragePermissionError("Jogosultsági hiba")

        # TimeoutError
        with pytest.raises(TimeoutError):
            raise TimeoutError("Időtúllépés")

        # ConnectionError
        with pytest.raises(ConnectionError):
            raise ConnectionError("Kapcsolódási hiba")

        # InsufficientDiskSpaceError
        with pytest.raises(InsufficientDiskSpaceError):
            raise InsufficientDiskSpaceError("Nincs elég lemezterület")

        # PermissionDeniedError
        with pytest.raises(PermissionDeniedError):
            raise PermissionDeniedError("Hozzáférés megtagadva")

    def test_exception_messages(self) -> None:
        """Teszteli a kivételek üzeneteit."""
        import pytest

        message = "Egyedi hibaüzenet"

        with pytest.raises(NeuralAIException) as exc_info:
            raise NeuralAIException(message)

        assert str(exc_info.value) == message
