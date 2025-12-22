"""Kivételek tesztelése a Neural AI Next projektben.

Ez a modul tartalmazza az összes kivétel osztály tesztjeit a
`neural_ai.core.base.exceptions` modulból.
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
    """NeuralAIException osztály tesztjei."""

    def test_kivetel_letrehozasa(self) -> None:
        """Teszteli a kivétel létrehozását."""
        exception = NeuralAIException("Hiba történt")
        assert str(exception) == "Hiba történt"

    def test_kivetel_okozasa(self) -> None:
        """Teszteli a kivétel dobását."""
        with pytest.raises(NeuralAIException) as exc_info:
            raise NeuralAIException("Teszt hiba")
        assert str(exc_info.value) == "Teszt hiba"


class TestStorageException:
    """StorageException osztály tesztjei."""

    def test_kivetel_letrehozasa(self) -> None:
        """Teszteli a kivétel létrehozását."""
        exception = StorageException("Tárolási hiba")
        assert str(exception) == "Tárolási hiba"
        assert isinstance(exception, NeuralAIException)

    def test_kivetel_okozasa(self) -> None:
        """Teszteli a kivétel dobását."""
        with pytest.raises(StorageException):
            raise StorageException("Tárolási hiba")


class TestStorageWriteError:
    """StorageWriteError osztály tesztjei."""

    def test_kivetel_letrehozasa(self) -> None:
        """Teszteli a kivétel létrehozását."""
        exception = StorageWriteError("Írási hiba")
        assert str(exception) == "Írási hiba"
        assert isinstance(exception, StorageException)

    def test_kivetel_okozasa(self) -> None:
        """Teszteli a kivétel dobását."""
        with pytest.raises(StorageWriteError):
            raise StorageWriteError("Írási hiba")


class TestStorageReadError:
    """StorageReadError osztály tesztjei."""

    def test_kivetel_letrehozasa(self) -> None:
        """Teszteli a kivétel létrehozását."""
        exception = StorageReadError("Olvasási hiba")
        assert str(exception) == "Olvasási hiba"
        assert isinstance(exception, StorageException)

    def test_kivetel_okozasa(self) -> None:
        """Teszteli a kivétel dobását."""
        with pytest.raises(StorageReadError):
            raise StorageReadError("Olvasási hiba")


class TestStoragePermissionError:
    """StoragePermissionError osztály tesztjei."""

    def test_kivetel_letrehozasa(self) -> None:
        """Teszteli a kivétel létrehozását."""
        exception = StoragePermissionError("Jogosultsági hiba")
        assert str(exception) == "Jogosultsági hiba"
        assert isinstance(exception, StorageException)

    def test_kivetel_okozasa(self) -> None:
        """Teszteli a kivétel dobását."""
        with pytest.raises(StoragePermissionError):
            raise StoragePermissionError("Jogosultsági hiba")


class TestConfigurationError:
    """ConfigurationError osztály tesztjei."""

    def test_kivetel_letrehozasa(self) -> None:
        """Teszteli a kivétel létrehozását."""
        exception = ConfigurationError("Konfigurációs hiba")
        assert str(exception) == "Konfigurációs hiba"
        assert isinstance(exception, NeuralAIException)

    def test_kivetel_okozasa(self) -> None:
        """Teszteli a kivétel dobását."""
        with pytest.raises(ConfigurationError):
            raise ConfigurationError("Konfigurációs hiba")


class TestDependencyError:
    """DependencyError osztály tesztjei."""

    def test_kivetel_letrehozasa(self) -> None:
        """Teszteli a kivétel létrehozását."""
        exception = DependencyError("Függőségi hiba")
        assert str(exception) == "Függőségi hiba"
        assert isinstance(exception, NeuralAIException)

    def test_kivetel_okozasa(self) -> None:
        """Teszteli a kivétel dobását."""
        with pytest.raises(DependencyError):
            raise DependencyError("Függőségi hiba")


class TestSingletonViolationError:
    """SingletonViolationError osztály tesztjei."""

    def test_kivetel_letrehozasa(self) -> None:
        """Teszteli a kivétel létrehozását."""
        exception = SingletonViolationError("Singleton megsértése")
        assert str(exception) == "Singleton megsértése"
        assert isinstance(exception, NeuralAIException)

    def test_kivetel_okozasa(self) -> None:
        """Teszteli a kivétel dobását."""
        with pytest.raises(SingletonViolationError):
            raise SingletonViolationError("Singleton megsértése")


class TestComponentNotFoundError:
    """ComponentNotFoundError osztály tesztjei."""

    def test_kivetel_letrehozasa(self) -> None:
        """Teszteli a kivétel létrehozását."""
        exception = ComponentNotFoundError("Komponens nem található")
        assert str(exception) == "Komponens nem található"
        assert isinstance(exception, NeuralAIException)

    def test_kivetel_okozasa(self) -> None:
        """Teszteli a kivétel dobását."""
        with pytest.raises(ComponentNotFoundError):
            raise ComponentNotFoundError("Komponens nem található")


class TestNetworkException:
    """NetworkException osztály tesztjei."""

    def test_kivetel_letrehozasa(self) -> None:
        """Teszteli a kivétel létrehozását."""
        exception = NetworkException("Hálózati hiba")
        assert str(exception) == "Hálózati hiba"
        assert isinstance(exception, NeuralAIException)

    def test_kivetel_okozasa(self) -> None:
        """Teszteli a kivétel dobását."""
        with pytest.raises(NetworkException):
            raise NetworkException("Hálózati hiba")


class TestTimeoutError:
    """TimeoutError osztály tesztjei."""

    def test_kivetel_letrehozasa(self) -> None:
        """Teszteli a kivétel létrehozását."""
        exception = TimeoutError("Időtúllépés")
        assert str(exception) == "Időtúllépés"
        assert isinstance(exception, NetworkException)

    def test_kivetel_okozasa(self) -> None:
        """Teszteli a kivétel dobását."""
        with pytest.raises(TimeoutError):
            raise TimeoutError("Időtúllépés")


class TestConnectionError:
    """ConnectionError osztály tesztjei."""

    def test_kivetel_letrehozasa(self) -> None:
        """Teszteli a kivétel létrehozását."""
        exception = ConnectionError("Kapcsolódási hiba")
        assert str(exception) == "Kapcsolódási hiba"
        assert isinstance(exception, NetworkException)

    def test_kivetel_okozasa(self) -> None:
        """Teszteli a kivétel dobását."""
        with pytest.raises(ConnectionError):
            raise ConnectionError("Kapcsolódási hiba")


class TestInsufficientDiskSpaceError:
    """InsufficientDiskSpaceError osztály tesztjei."""

    def test_kivetel_letrehozasa(self) -> None:
        """Teszteli a kivétel létrehozását."""
        exception = InsufficientDiskSpaceError("Nincs elég hely")
        assert str(exception) == "Nincs elég hely"
        assert isinstance(exception, StorageException)

    def test_kivetel_okozasa(self) -> None:
        """Teszteli a kivétel dobását."""
        with pytest.raises(InsufficientDiskSpaceError):
            raise InsufficientDiskSpaceError("Nincs elég hely")


class TestPermissionDeniedError:
    """PermissionDeniedError osztály tesztjei."""

    def test_kivetel_letrehozasa(self) -> None:
        """Teszteli a kivétel létrehozását."""
        exception = PermissionDeniedError("Jogosultság megtagadva")
        assert str(exception) == "Jogosultság megtagadva"
        assert isinstance(exception, StorageException)

    def test_kivetel_okozasa(self) -> None:
        """Teszteli a kivétel dobását."""
        with pytest.raises(PermissionDeniedError):
            raise PermissionDeniedError("Jogosultság megtagadva")


class TestExceptionHierarchy:
    """Kivétel hierarchia tesztjei."""

    def test_storage_hierarchia(self) -> None:
        """Teszteli a tárolási kivételek hierarchiáját."""
        assert issubclass(StorageWriteError, StorageException)
        assert issubclass(StorageReadError, StorageException)
        assert issubclass(StoragePermissionError, StorageException)
        assert issubclass(InsufficientDiskSpaceError, StorageException)
        assert issubclass(PermissionDeniedError, StorageException)
        assert issubclass(StorageException, NeuralAIException)

    def test_network_hierarchia(self) -> None:
        """Teszteli a hálózati kivételek hierarchiáját."""
        assert issubclass(TimeoutError, NetworkException)
        assert issubclass(ConnectionError, NetworkException)
        assert issubclass(NetworkException, NeuralAIException)

    def test_base_hierarchia(self) -> None:
        """Teszteli az alap kivételek hierarchiáját."""
        assert issubclass(ConfigurationError, NeuralAIException)
        assert issubclass(DependencyError, NeuralAIException)
        assert issubclass(SingletonViolationError, NeuralAIException)
        assert issubclass(ComponentNotFoundError, NeuralAIException)