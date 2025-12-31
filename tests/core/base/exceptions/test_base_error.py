"""Base kivételek tesztelése.

Ez a modul tartalmazza a neural_ai.core.base.exceptions modulban
definiált összes kivétel osztály tesztjeit.
"""

import pytest

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


class TestNeuralAIException:
    """NeuralAIException alap kivétel tesztjei."""

    def test_base_exception_can_be_raised(self) -> None:
        """Teszteli, hogy az alap kivétel dobható-e."""
        with pytest.raises(NeuralAIException):
            raise NeuralAIException("Alap kivétel")

    def test_base_exception_with_message(self) -> None:
        """Teszteli a kivételt üzenettel."""
        message = "Teszt hibaüzenet"
        with pytest.raises(NeuralAIException) as exc_info:
            raise NeuralAIException(message)

        assert str(exc_info.value) == message

    def test_base_exception_inheritance(self) -> None:
        """Teszteli, hogy a kivétel az Exception osztályból származik."""
        assert issubclass(NeuralAIException, Exception)


class TestStorageException:
    """StorageException kivétel tesztjei."""

    def test_storage_exception_can_be_raised(self) -> None:
        """Teszteli, hogy a tároló kivétel dobható-e."""
        with pytest.raises(StorageException):
            raise StorageException("Tároló hiba")

    def test_storage_exception_inheritance(self) -> None:
        """Teszteli, hogy a kivétel a NeuralAIException-ből származik."""
        assert issubclass(StorageException, NeuralAIException)

    def test_storage_exception_with_message(self) -> None:
        """Teszteli a kivételt üzenettel."""
        message = "Tárolási hiba történt"
        with pytest.raises(StorageException) as exc_info:
            raise StorageException(message)

        assert str(exc_info.value) == message


class TestStorageWriteError:
    """StorageWriteError kivétel tesztjei."""

    def test_storage_write_error_can_be_raised(self) -> None:
        """Teszteli, hogy az írási hiba dobható-e."""
        with pytest.raises(StorageWriteError):
            raise StorageWriteError("Írási hiba")

    def test_storage_write_error_inheritance(self) -> None:
        """Teszteli az öröklődést."""
        assert issubclass(StorageWriteError, StorageException)
        assert issubclass(StorageWriteError, NeuralAIException)

    def test_storage_write_error_message(self) -> None:
        """Teszteli a hibaüzenetet."""
        message = "Nem sikerült írni a fájlba"
        with pytest.raises(StorageWriteError) as exc_info:
            raise StorageWriteError(message)

        assert str(exc_info.value) == message


class TestStorageReadError:
    """StorageReadError kivétel tesztjei."""

    def test_storage_read_error_can_be_raised(self) -> None:
        """Teszteli, hogy az olvasási hiba dobható-e."""
        with pytest.raises(StorageReadError):
            raise StorageReadError("Olvasási hiba")

    def test_storage_read_error_inheritance(self) -> None:
        """Teszteli az öröklődést."""
        assert issubclass(StorageReadError, StorageException)
        assert issubclass(StorageReadError, NeuralAIException)

    def test_storage_read_error_message(self) -> None:
        """Teszteli a hibaüzenetet."""
        message = "Nem sikerült olvasni a fájlból"
        with pytest.raises(StorageReadError) as exc_info:
            raise StorageReadError(message)

        assert str(exc_info.value) == message


class TestStoragePermissionError:
    """StoragePermissionError kivétel tesztjei."""

    def test_storage_permission_error_can_be_raised(self) -> None:
        """Teszteli, hogy a jogosultsági hiba dobható-e."""
        with pytest.raises(StoragePermissionError):
            raise StoragePermissionError("Jogosultsági hiba")

    def test_storage_permission_error_inheritance(self) -> None:
        """Teszteli az öröklődést."""
        assert issubclass(StoragePermissionError, StorageException)
        assert issubclass(StoragePermissionError, NeuralAIException)

    def test_storage_permission_error_message(self) -> None:
        """Teszteli a hibaüzenetet."""
        message = "Nincs jogosultság a művelethez"
        with pytest.raises(StoragePermissionError) as exc_info:
            raise StoragePermissionError(message)

        assert str(exc_info.value) == message


class TestConfigurationError:
    """ConfigurationError kivétel tesztjei."""

    def test_configuration_error_can_be_raised(self) -> None:
        """Teszteli, hogy a konfigurációs hiba dobható-e."""
        with pytest.raises(ConfigurationError):
            raise ConfigurationError("Konfigurációs hiba")

    def test_configuration_error_inheritance(self) -> None:
        """Teszteli az öröklődést."""
        assert issubclass(ConfigurationError, NeuralAIException)

    def test_configuration_error_message(self) -> None:
        """Teszteli a hibaüzenetet."""
        message = "Érvénytelen konfiguráció"
        with pytest.raises(ConfigurationError) as exc_info:
            raise ConfigurationError(message)

        assert str(exc_info.value) == message


class TestDependencyError:
    """DependencyError kivétel tesztjei."""

    def test_dependency_error_can_be_raised(self) -> None:
        """Teszteli, hogy a függőségi hiba dobható-e."""
        with pytest.raises(DependencyError):
            raise DependencyError("Függőségi hiba")

    def test_dependency_error_inheritance(self) -> None:
        """Teszteli az öröklődést."""
        assert issubclass(DependencyError, NeuralAIException)

    def test_dependency_error_message(self) -> None:
        """Teszteli a hibaüzenetet."""
        message = "Hiányzó függőség"
        with pytest.raises(DependencyError) as exc_info:
            raise DependencyError(message)

        assert str(exc_info.value) == message


class TestSingletonViolationError:
    """SingletonViolationError kivétel tesztjei."""

    def test_singleton_violation_error_can_be_raised(self) -> None:
        """Teszteli, hogy a singleton megsértésének hibája dobható-e."""
        with pytest.raises(SingletonViolationError):
            raise SingletonViolationError("Singleton megsértése")

    def test_singleton_violation_error_inheritance(self) -> None:
        """Teszteli az öröklődést."""
        assert issubclass(SingletonViolationError, NeuralAIException)

    def test_singleton_violation_error_message(self) -> None:
        """Teszteli a hibaüzenetet."""
        message = "A singleton minta megsérült"
        with pytest.raises(SingletonViolationError) as exc_info:
            raise SingletonViolationError(message)

        assert str(exc_info.value) == message


class TestComponentNotFoundError:
    """ComponentNotFoundError kivétel tesztjei."""

    def test_component_not_found_error_can_be_raised(self) -> None:
        """Teszteli, hogy a komponens nem található hiba dobható-e."""
        with pytest.raises(ComponentNotFoundError):
            raise ComponentNotFoundError("Komponens nem található")

    def test_component_not_found_error_inheritance(self) -> None:
        """Teszteli az öröklődést."""
        assert issubclass(ComponentNotFoundError, NeuralAIException)

    def test_component_not_found_error_message(self) -> None:
        """Teszteli a hibaüzenetet."""
        message = "A kért komponens nem található"
        with pytest.raises(ComponentNotFoundError) as exc_info:
            raise ComponentNotFoundError(message)

        assert str(exc_info.value) == message


class TestNetworkException:
    """NetworkException kivétel tesztjei."""

    def test_network_exception_can_be_raised(self) -> None:
        """Teszteli, hogy a hálózati kivétel dobható-e."""
        with pytest.raises(NetworkException):
            raise NetworkException("Hálózati hiba")

    def test_network_exception_inheritance(self) -> None:
        """Teszteli az öröklődést."""
        assert issubclass(NetworkException, NeuralAIException)

    def test_network_exception_message(self) -> None:
        """Teszteli a hibaüzenetet."""
        message = "Hálózati kommunikációs hiba"
        with pytest.raises(NetworkException) as exc_info:
            raise NetworkException(message)

        assert str(exc_info.value) == message


class TestTimeoutError:
    """TimeoutError kivétel tesztjei."""

    def test_timeout_error_can_be_raised(self) -> None:
        """Teszteli, hogy az időtúllépési hiba dobható-e."""
        with pytest.raises(TimeoutError):
            raise TimeoutError("Időtúllépés")

    def test_timeout_error_inheritance(self) -> None:
        """Teszteli az öröklődést."""
        assert issubclass(TimeoutError, NetworkException)
        assert issubclass(TimeoutError, NeuralAIException)

    def test_timeout_error_message(self) -> None:
        """Teszteli a hibaüzenetet."""
        message = "A művelet túllépte az időkeretet"
        with pytest.raises(TimeoutError) as exc_info:
            raise TimeoutError(message)

        assert str(exc_info.value) == message


class TestConnectionError:
    """ConnectionError kivétel tesztjei."""

    def test_connection_error_can_be_raised(self) -> None:
        """Teszteli, hogy a kapcsolódási hiba dobható-e."""
        with pytest.raises(ConnectionError):
            raise ConnectionError("Kapcsolódási hiba")

    def test_connection_error_inheritance(self) -> None:
        """Teszteli az öröklődést."""
        assert issubclass(ConnectionError, NetworkException)
        assert issubclass(ConnectionError, NeuralAIException)

    def test_connection_error_message(self) -> None:
        """Teszteli a hibaüzenetet."""
        message = "Nem sikerült kapcsolódni a szerverhez"
        with pytest.raises(ConnectionError) as exc_info:
            raise ConnectionError(message)

        assert str(exc_info.value) == message


class TestInsufficientDiskSpaceError:
    """InsufficientDiskSpaceError kivétel tesztjei."""

    def test_insufficient_disk_space_error_can_be_raised(self) -> None:
        """Teszteli, hogy a lemezterület hiány hiba dobható-e."""
        with pytest.raises(InsufficientDiskSpaceError):
            raise InsufficientDiskSpaceError("Nincs elég hely")

    def test_insufficient_disk_space_error_inheritance(self) -> None:
        """Teszteli az öröklődést."""
        assert issubclass(InsufficientDiskSpaceError, StorageException)
        assert issubclass(InsufficientDiskSpaceError, NeuralAIException)

    def test_insufficient_disk_space_error_message(self) -> None:
        """Teszteli a hibaüzenetet."""
        message = "Nincs elég szabad lemezterület"
        with pytest.raises(InsufficientDiskSpaceError) as exc_info:
            raise InsufficientDiskSpaceError(message)

        assert str(exc_info.value) == message


class TestPermissionDeniedError:
    """PermissionDeniedError kivétel tesztjei."""

    def test_permission_denied_error_can_be_raised(self) -> None:
        """Teszteli, hogy a jogosultság megtagadva hiba dobható-e."""
        with pytest.raises(PermissionDeniedError):
            raise PermissionDeniedError("Jogosultság megtagadva")

    def test_permission_denied_error_inheritance(self) -> None:
        """Teszteli az öröklődést."""
        assert issubclass(PermissionDeniedError, StorageException)
        assert issubclass(PermissionDeniedError, NeuralAIException)

    def test_permission_denied_error_message(self) -> None:
        """Teszteli a hibaüzenetet."""
        message = "A hozzáférés megtagadva"
        with pytest.raises(PermissionDeniedError) as exc_info:
            raise PermissionDeniedError(message)

        assert str(exc_info.value) == message
