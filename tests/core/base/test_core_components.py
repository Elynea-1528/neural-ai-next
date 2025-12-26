"""Tesztek a CoreComponents és LazyLoader osztályokhoz."""

import warnings
from collections.abc import Callable
from typing import Any, Optional
from unittest.mock import Mock

import pytest

from neural_ai.core.base.implementations.component_bundle import CoreComponents
from neural_ai.core.base.implementations.lazy_loader import LazyLoader
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
from neural_ai.core.storage.interfaces.storage_interface import StorageInterface


def suppress_singleton_warnings(test_func: Callable[..., Any]) -> Callable[..., Any]:
    """Dekorátor a singleton ellenőrzés figyelmeztetéseinek elnyomásához."""

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        with warnings.catch_warnings():
            warnings.filterwarnings(
                "ignore",
                message="Component .* not properly registered in container",
                category=UserWarning,
            )
            return test_func(*args, **kwargs)

    return wrapper


class SingletonMock(Mock):
    """Mock osztály, amely megfelel a DIContainer singleton ellenőrzésének.

    Ez a mock minden példányosításkor új objektumot hoz létre (nem valódi singleton),
    de rendelkezik a szükséges attribútumokkal, hogy átmenjen a DIContainer
    singleton ellenőrzésén.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Inicializálás, minden példány új objektum."""
        super().__init__(*args, **kwargs)
        # Szükséges attribútumok a DIContainer ellenőrzéséhez
        self._initialized = True

    # Osztályszintű attribútum a singleton ellenőrzéshez
    _instance: Optional["SingletonMock"] = None


class TestLazyLoader:
    """Lusta betöltő tesztelése."""

    def test_lazy_loader_initial_state(self) -> None:
        """Teszteli a lusta betöltő kezdeti állapotát."""

        # Arrange
        def loader_func() -> str:
            return "test_value"

        # Act
        loader = LazyLoader(loader_func)

        # Assert
        assert not loader.is_loaded
        # Ne ellenőrizzük a _value-t, mert az protected

    def test_lazy_loader_call_loads_value(self) -> None:
        """Teszteli, hogy a hívás betölti az értéket."""

        # Arrange
        def loader_func() -> str:
            return "test_value"

        loader = LazyLoader(loader_func)

        # Act
        result = loader()

        # Assert
        assert result == "test_value"
        assert loader.is_loaded
        # A _value protected, csak a publikus API-t használjuk

    def test_lazy_loader_call_caches_value(self) -> None:
        """Teszteli, hogy a érték gyorsítótárazódik."""
        # Arrange
        call_count = 0

        def loader_func() -> int:
            nonlocal call_count
            call_count += 1
            return 42

        loader = LazyLoader(loader_func)

        # Act
        result1 = loader()
        result2 = loader()
        result3 = loader()

        # Assert
        assert result1 == 42
        assert result2 == 42
        assert result3 == 42
        assert call_count == 1  # Csak egyszer hívódik meg

    def test_lazy_loader_reset(self) -> None:
        """Teszteli a betöltő visszaállítását."""

        # Arrange
        def loader_func() -> str:
            return "test_value"

        loader = LazyLoader(loader_func)
        loader()  # Betöltjük

        # Act
        loader.reset()

        # Assert
        assert not loader.is_loaded
        # A _value protected, csak a publikus API-t használjuk

    def test_lazy_loader_reset_and_reload(self) -> None:
        """Teszteli a visszaállítás utáni újrabetöltést."""
        # Arrange
        call_count = 0

        def loader_func() -> int:
            nonlocal call_count
            call_count += 1
            return call_count

        loader = LazyLoader(loader_func)

        # Act
        result1 = loader()  # Először betöltés
        loader.reset()
        result2 = loader()  # Újrabetöltés

        # Assert
        assert result1 == 1
        assert result2 == 2
        assert call_count == 2


class TestCoreComponents:
    """Alap komponensek tesztelése."""

    def test_core_components_initialization_without_container(self) -> None:
        """Teszteli a komponensek inicializálását konténer nélkül."""
        # Act
        components = CoreComponents()

        # Assert
        # A _container és _factory protected tagok, csak a publikus API-t használjuk
        assert components.config is None  # Alapértelmezett konténer üres
        assert components.logger is None
        assert components.storage is None

    def test_core_components_initialization_with_container(self) -> None:
        """Teszteli a komponensek inicializálását megadott konténerrel."""
        # Arrange
        from neural_ai.core.base.implementations.di_container import DIContainer

        container = DIContainer()

        # Act
        components = CoreComponents(container)

        # Assert
        # A _container protected, csak a publikus API-t használjuk
        # A konténer jelenlétét a komponensek lekérdezésével ellenőrizzük
        assert components.config is None
        assert components.logger is None
        assert components.storage is None

    def test_config_property_returns_none_when_not_registered(self) -> None:
        """Teszteli, hogy a config property None-t ad vissza, ha nincs regisztrálva."""
        # Arrange
        components = CoreComponents()

        # Act
        result = components.config

        # Assert
        assert result is None

    @suppress_singleton_warnings
    def test_config_property_returns_instance_when_registered(self) -> None:
        """Teszteli, hogy a config property visszaadja a példányt, ha regisztrálva van."""
        # Arrange
        components = CoreComponents()
        config_mock = SingletonMock(spec=ConfigManagerInterface)
        components.set_config(config_mock)

        # Act
        result = components.config

        # Assert
        assert result is config_mock

    def test_logger_property_returns_none_when_not_registered(self) -> None:
        """Teszteli, hogy a logger property None-t ad vissza, ha nincs regisztrálva."""
        # Arrange
        components = CoreComponents()

        # Act
        result = components.logger

        # Assert
        assert result is None

    @suppress_singleton_warnings
    def test_logger_property_returns_instance_when_registered(self) -> None:
        """Teszteli, hogy a logger property visszaadja a példányt, ha regisztrálva van."""
        # Arrange
        components = CoreComponents()
        logger_mock = SingletonMock(spec=LoggerInterface)
        components.set_logger(logger_mock)

        # Act
        result = components.logger

        # Assert
        assert result is logger_mock

    def test_storage_property_returns_none_when_not_registered(self) -> None:
        """Teszteli, hogy a storage property None-t ad vissza, ha nincs regisztrálva."""
        # Arrange
        components = CoreComponents()

        # Act
        result = components.storage

        # Assert
        assert result is None

    @suppress_singleton_warnings
    def test_storage_property_returns_instance_when_registered(self) -> None:
        """Teszteli, hogy a storage property visszaadja a példányt, ha regisztrálva van."""
        # Arrange
        components = CoreComponents()
        storage_mock = SingletonMock(spec=StorageInterface)
        components.set_storage(storage_mock)

        # Act
        result = components.storage

        # Assert
        assert result is storage_mock

    @suppress_singleton_warnings
    def test_set_config_registers_instance(self) -> None:
        """Teszteli a konfiguráció beállítását."""
        # Arrange
        components = CoreComponents()
        config_mock = SingletonMock(spec=ConfigManagerInterface)

        # Act
        components.set_config(config_mock)

        # Assert
        assert components.config is config_mock

    @suppress_singleton_warnings
    def test_set_logger_registers_instance(self) -> None:
        """Teszteli a logger beállítását."""
        # Arrange
        components = CoreComponents()
        logger_mock = SingletonMock(spec=LoggerInterface)

        # Act
        components.set_logger(logger_mock)

        # Assert
        assert components.logger is logger_mock

    @suppress_singleton_warnings
    def test_set_storage_registers_instance(self) -> None:
        """Teszteli a tároló beállítását."""
        # Arrange
        components = CoreComponents()
        storage_mock = SingletonMock(spec=StorageInterface)

        # Act
        components.set_storage(storage_mock)

        # Assert
        assert components.storage is storage_mock

    def test_has_config_returns_false_when_not_present(self) -> None:
        """Teszteli, hogy has_config False-t ad vissza, ha nincs config."""
        # Arrange
        components = CoreComponents()

        # Act
        result = components.has_config()

        # Assert
        assert result is False

    @suppress_singleton_warnings
    def test_has_config_returns_true_when_present(self) -> None:
        """Teszteli, hogy has_config True-t ad vissza, ha van config."""
        # Arrange
        components = CoreComponents()
        config_mock = SingletonMock(spec=ConfigManagerInterface)
        components.set_config(config_mock)

        # Act
        result = components.has_config()

        # Assert
        assert result is True

    def test_has_logger_returns_false_when_not_present(self) -> None:
        """Teszteli, hogy has_logger False-t ad vissza, ha nincs logger."""
        # Arrange
        components = CoreComponents()

        # Act
        result = components.has_logger()

        # Assert
        assert result is False

    @suppress_singleton_warnings
    def test_has_logger_returns_true_when_present(self) -> None:
        """Teszteli, hogy has_logger True-t ad vissza, ha van logger."""
        # Arrange
        components = CoreComponents()
        logger_mock = SingletonMock(spec=LoggerInterface)
        components.set_logger(logger_mock)

        # Act
        result = components.has_logger()

        # Assert
        assert result is True

    def test_has_storage_returns_false_when_not_present(self) -> None:
        """Teszteli, hogy has_storage False-t ad vissza, ha nincs storage."""
        # Arrange
        components = CoreComponents()

        # Act
        result = components.has_storage()

        # Assert
        assert result is False

    @suppress_singleton_warnings
    def test_has_storage_returns_true_when_present(self) -> None:
        """Teszteli, hogy has_storage True-t ad vissza, ha van storage."""
        # Arrange
        components = CoreComponents()
        storage_mock = SingletonMock(spec=StorageInterface)
        components.set_storage(storage_mock)

        # Act
        result = components.has_storage()

        # Assert
        assert result is True

    def test_validate_returns_false_when_no_components(self) -> None:
        """Teszteli, hogy validate False-t ad vissza, ha nincsenek komponensek."""
        # Arrange
        components = CoreComponents()

        # Act
        result = components.validate()

        # Assert
        assert result is False

    @suppress_singleton_warnings
    def test_validate_returns_false_when_some_components_missing(self) -> None:
        """Teszteli, hogy validate False-t ad vissza, ha néhány komponens hiányzik."""
        # Arrange
        components = CoreComponents()
        config_mock = SingletonMock(spec=ConfigManagerInterface)
        components.set_config(config_mock)

        # Act
        result = components.validate()

        # Assert
        assert result is False

    @suppress_singleton_warnings
    def test_validate_returns_true_when_all_components_present(self) -> None:
        """Teszteli, hogy validate True-t ad vissza, ha minden komponens megvan."""
        # Arrange
        from neural_ai.core.db.implementations.sqlalchemy_session import DatabaseManager
        from neural_ai.core.events.implementations.zeromq_bus import EventBus
        from neural_ai.core.utils.implementations.hardware_info import HardwareInfo

        components = CoreComponents()
        config_mock = SingletonMock(spec=ConfigManagerInterface)
        logger_mock = SingletonMock(spec=LoggerInterface)
        storage_mock = SingletonMock(spec=StorageInterface)
        database_mock = SingletonMock(spec=DatabaseManager)
        event_bus_mock = SingletonMock(spec=EventBus)
        hardware_mock = SingletonMock(spec=HardwareInfo)

        components.set_config(config_mock)
        components.set_logger(logger_mock)
        components.set_storage(storage_mock)
        components.set_database(database_mock)
        components.set_event_bus(event_bus_mock)
        components.set_hardware(hardware_mock)

        # Act
        result = components.validate()

        # Assert
        assert result is True

    @suppress_singleton_warnings
    def test_validate_returns_false_when_only_config_and_logger(self) -> None:
        """Teszteli, hogy validate False-t ad vissza, ha csak config és logger van."""
        # Arrange
        components = CoreComponents()
        config_mock = SingletonMock(spec=ConfigManagerInterface)
        logger_mock = SingletonMock(spec=LoggerInterface)

        components.set_config(config_mock)
        components.set_logger(logger_mock)

        # Act
        result = components.validate()

        # Assert
        assert result is False

    @suppress_singleton_warnings
    def test_validate_returns_false_when_only_config_and_storage(self) -> None:
        """Teszteli, hogy validate False-t ad vissza, ha csak config és storage van."""
        # Arrange
        components = CoreComponents()
        config_mock = SingletonMock(spec=ConfigManagerInterface)
        storage_mock = SingletonMock(spec=StorageInterface)

        components.set_config(config_mock)
        components.set_storage(storage_mock)

        # Act
        result = components.validate()

        # Assert
        assert result is False

    @suppress_singleton_warnings
    def test_validate_returns_false_when_only_logger_and_storage(self) -> None:
        """Teszteli, hogy validate False-t ad vissza, ha csak logger és storage van."""
        # Arrange
        components = CoreComponents()
        logger_mock = SingletonMock(spec=LoggerInterface)
        storage_mock = SingletonMock(spec=StorageInterface)

        components.set_logger(logger_mock)
        components.set_storage(storage_mock)

        # Act
        result = components.validate()

        # Assert
        assert result is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
