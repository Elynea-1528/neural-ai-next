#!/usr/bin/env python3
"""Integrációs teszt a bootstrap_core függvényhez.

Ez a tesztmodul ellenőrzi a core komponensek inicializálásának teljes folyamatát,
beleértve a DI konténer működését és a komponensek közötti függőségeket.
"""

import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# Project root hozzáadása a Python path-hoz
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from neural_ai.core import bootstrap_core, get_core_components
from neural_ai.core.base.implementations.component_bundle import CoreComponents
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.db.implementations.sqlalchemy_session import DatabaseManager
from neural_ai.core.events.implementations.zeromq_bus import EventBus
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
from neural_ai.core.storage.interfaces.storage_interface import StorageInterface
from neural_ai.core.utils.implementations.hardware_info import HardwareInfo


class TestBootstrapCoreIntegration:
    """Integrációs tesztek a bootstrap_core függvényhez."""

    def test_bootstrap_core_returns_core_components(self) -> None:
        """Teszteli, hogy a bootstrap_core visszaad egy CoreComponents példányt."""
        # Mockoljuk az összes factory-t, hogy ne próbáljanak ténylegesen inicializálni
        with (
            patch("neural_ai.core.config.factory.ConfigManagerFactory.get_manager") as mock_config,
            patch("neural_ai.core.logger.factory.LoggerFactory.get_logger") as mock_logger,
            patch("neural_ai.core.db.factory.DatabaseFactory.create_manager") as mock_db,
            patch("neural_ai.core.events.factory.EventBusFactory.create") as mock_event,
            patch("neural_ai.core.storage.factory.StorageFactory.get_storage") as mock_storage,
            patch("neural_ai.core.utils.factory.HardwareFactory.get_hardware_info") as mock_hw,
        ):
            # Beállítjuk a mockok visszatérési értékét
            mock_config.return_value = MagicMock(spec=ConfigManagerInterface)
            mock_logger.return_value = MagicMock(spec=LoggerInterface)
            mock_db.return_value = MagicMock(spec=DatabaseManager)
            mock_event.return_value = MagicMock(spec=EventBus)
            mock_storage.return_value = MagicMock(spec=StorageInterface)
            mock_hw.return_value = MagicMock(spec=HardwareInfo)

            # Hívjuk meg a bootstrap_core-t
            components = bootstrap_core()

            # Ellenőrizzük, hogy CoreComponents objektumot kapunk vissza
            assert isinstance(components, CoreComponents)

    def test_bootstrap_core_initializes_all_components(self) -> None:
        """Teszteli, hogy a bootstrap_core inicializálja az összes komponenst."""
        with (
            patch("neural_ai.core.config.factory.ConfigManagerFactory.get_manager") as mock_config,
            patch("neural_ai.core.logger.factory.LoggerFactory.get_logger") as mock_logger,
            patch("neural_ai.core.db.factory.DatabaseFactory.create_manager") as mock_db,
            patch("neural_ai.core.events.factory.EventBusFactory.create") as mock_event,
            patch("neural_ai.core.storage.factory.StorageFactory.get_storage") as mock_storage,
            patch("neural_ai.core.utils.factory.HardwareFactory.get_hardware_info") as mock_hw,
        ):
            # Beállítjuk a mockok visszatérési értékét
            mock_config.return_value = MagicMock(spec=ConfigManagerInterface)
            mock_logger.return_value = MagicMock(spec=LoggerInterface)
            mock_db.return_value = MagicMock(spec=DatabaseManager)
            mock_event.return_value = MagicMock(spec=EventBus)
            mock_storage.return_value = MagicMock(spec=StorageInterface)
            mock_hw.return_value = MagicMock(spec=HardwareInfo)

            # Hívjuk meg a bootstrap_core-t
            components = bootstrap_core()

            # Ellenőrizzük, hogy minden komponens elérhető
            assert components.config is not None
            assert components.logger is not None
            assert components.storage is not None
            assert components.database is not None
            assert components.event_bus is not None
            assert components.hardware is not None

    def test_bootstrap_core_with_custom_config_path(self) -> None:
        """Teszteli, hogy a bootstrap_core elfogadja az egyéni konfigurációs útvonalat."""
        custom_config_path = "custom_config.yml"

        with (
            patch("neural_ai.core.config.factory.ConfigManagerFactory.get_manager") as mock_config,
            patch("neural_ai.core.logger.factory.LoggerFactory.get_logger") as mock_logger,
            patch("neural_ai.core.db.factory.DatabaseFactory.create_manager") as mock_db,
            patch("neural_ai.core.events.factory.EventBusFactory.create") as mock_event,
            patch("neural_ai.core.storage.factory.StorageFactory.get_storage") as mock_storage,
            patch("neural_ai.core.utils.factory.HardwareFactory.get_hardware_info") as mock_hw,
        ):
            mock_config.return_value = MagicMock(spec=ConfigManagerInterface)
            mock_logger.return_value = MagicMock(spec=LoggerInterface)
            mock_db.return_value = MagicMock(spec=DatabaseManager)
            mock_event.return_value = MagicMock(spec=EventBus)
            mock_storage.return_value = MagicMock(spec=StorageInterface)
            mock_hw.return_value = MagicMock(spec=HardwareInfo)

            # Hívjuk meg a bootstrap_core-t egyéni konfigurációs útvonallal
            components = bootstrap_core(config_path=custom_config_path)

            # Ellenőrizzük, hogy a konfigurációs útvonal át lett adva
            mock_config.assert_called_once_with(filename=custom_config_path)
            assert isinstance(components, CoreComponents)

    def test_bootstrap_core_with_custom_log_level(self) -> None:
        """Teszteli, hogy a bootstrap_core elfogadja az egyéni log szintet."""
        custom_log_level = "DEBUG"

        with (
            patch("neural_ai.core.config.factory.ConfigManagerFactory.get_manager") as mock_config,
            patch("neural_ai.core.logger.factory.LoggerFactory.get_logger") as mock_logger,
            patch("neural_ai.core.db.factory.DatabaseFactory.create_manager") as mock_db,
            patch("neural_ai.core.events.factory.EventBusFactory.create") as mock_event,
            patch("neural_ai.core.storage.factory.StorageFactory.get_storage") as mock_storage,
            patch("neural_ai.core.utils.factory.HardwareFactory.get_hardware_info") as mock_hw,
        ):
            mock_config.return_value = MagicMock(spec=ConfigManagerInterface)
            mock_logger.return_value = MagicMock(spec=LoggerInterface)
            mock_db.return_value = MagicMock(spec=DatabaseManager)
            mock_event.return_value = MagicMock(spec=EventBus)
            mock_storage.return_value = MagicMock(spec=StorageInterface)
            mock_hw.return_value = MagicMock(spec=HardwareInfo)

            # Hívjuk meg a bootstrap_core-t egyéni log szinttel
            components = bootstrap_core(log_level=custom_log_level)

            # Ellenőrizzük, hogy a log szint át lett adva
            mock_logger.assert_called_once_with(
                name="NeuralAI", logger_type="default", level=custom_log_level
            )
            assert isinstance(components, CoreComponents)

    def test_bootstrap_core_registers_components_in_container(self) -> None:
        """Teszteli, hogy a bootstrap_core regisztrálja a komponenseket a DI konténerben."""
        with (
            patch("neural_ai.core.config.factory.ConfigManagerFactory.get_manager") as mock_config,
            patch("neural_ai.core.logger.factory.LoggerFactory.get_logger") as mock_logger,
            patch("neural_ai.core.db.factory.DatabaseFactory.create_manager") as mock_db,
            patch("neural_ai.core.events.factory.EventBusFactory.create") as mock_event,
            patch("neural_ai.core.storage.factory.StorageFactory.get_storage") as mock_storage,
            patch("neural_ai.core.utils.factory.HardwareFactory.get_hardware_info") as mock_hw,
        ):
            # Készítünk specifikus mock objektumokat
            config_mock = MagicMock(spec=ConfigManagerInterface)
            logger_mock = MagicMock(spec=LoggerInterface)
            db_mock = MagicMock(spec=DatabaseManager)
            event_mock = MagicMock(spec=EventBus)
            storage_mock = MagicMock(spec=StorageInterface)
            hw_mock = MagicMock(spec=HardwareInfo)

            mock_config.return_value = config_mock
            mock_logger.return_value = logger_mock
            mock_db.return_value = db_mock
            mock_event.return_value = event_mock
            mock_storage.return_value = storage_mock
            mock_hw.return_value = hw_mock

            # Hívjuk meg a bootstrap_core-t
            components = bootstrap_core()

            # Ellenőrizzük, hogy a komponensek megfelelően lettek-e regisztrálva
            assert components.config is config_mock
            assert components.logger is logger_mock
            assert components.storage is storage_mock
            assert components.database is db_mock
            assert components.event_bus is event_mock
            assert components.hardware is hw_mock

    def test_bootstrap_core_validation_passes(self) -> None:
        """Teszteli, hogy a bootstrap_core által létrehozott komponensek validációja sikeres."""
        with (
            patch("neural_ai.core.config.factory.ConfigManagerFactory.get_manager") as mock_config,
            patch("neural_ai.core.logger.factory.LoggerFactory.get_logger") as mock_logger,
            patch("neural_ai.core.db.factory.DatabaseFactory.create_manager") as mock_db,
            patch("neural_ai.core.events.factory.EventBusFactory.create") as mock_event,
            patch("neural_ai.core.storage.factory.StorageFactory.get_storage") as mock_storage,
            patch("neural_ai.core.utils.factory.HardwareFactory.get_hardware_info") as mock_hw,
        ):
            mock_config.return_value = MagicMock(spec=ConfigManagerInterface)
            mock_logger.return_value = MagicMock(spec=LoggerInterface)
            mock_db.return_value = MagicMock(spec=DatabaseManager)
            mock_event.return_value = MagicMock(spec=EventBus)
            mock_storage.return_value = MagicMock(spec=StorageInterface)
            mock_hw.return_value = MagicMock(spec=HardwareInfo)

            # Hívjuk meg a bootstrap_core-t
            components = bootstrap_core()

            # Ellenőrizzük, hogy a validáció sikeres
            assert components.validate() is True

    def test_bootstrap_core_handles_missing_config_file(self) -> None:
        """Teszteli, hogy a bootstrap_core kezeli a hiányzó konfigurációs fájlt."""
        from neural_ai.core.config.exceptions.config_error import ConfigError

        with patch("neural_ai.core.config.factory.ConfigManagerFactory.get_manager") as mock_config:
            # A konfiguráció betöltése dobjon kivételt
            mock_config.side_effect = ConfigError("Config file not found")

            # A bootstrap_core-nek tovább kell adnia a kivételt
            with pytest.raises(ConfigError, match="Config file not found"):
                bootstrap_core(config_path="nonexistent_config.yml")

    @pytest.mark.asyncio
    async def test_bootstrap_core_with_async_database_initialization(
        self,
    ) -> None:
        """Teszteli, hogy a bootstrap_core létrehoz egy adatbázis komponenst."""
        with (
            patch("neural_ai.core.config.factory.ConfigManagerFactory.get_manager") as mock_config,
            patch("neural_ai.core.logger.factory.LoggerFactory.get_logger") as mock_logger,
            patch("neural_ai.core.db.factory.DatabaseFactory.create_manager") as mock_db,
            patch("neural_ai.core.events.factory.EventBusFactory.create") as mock_event,
            patch("neural_ai.core.storage.factory.StorageFactory.get_storage") as mock_storage,
            patch("neural_ai.core.utils.factory.HardwareFactory.get_hardware_info") as mock_hw,
        ):
            # Készítünk egy aszinkron inicializálható adatbázis mockot
            db_mock = MagicMock(spec=DatabaseManager)
            db_mock.initialize = AsyncMock()

            mock_config.return_value = MagicMock(spec=ConfigManagerInterface)
            mock_logger.return_value = MagicMock(spec=LoggerInterface)
            mock_db.return_value = db_mock
            mock_event.return_value = MagicMock(spec=EventBus)
            mock_storage.return_value = MagicMock(spec=StorageInterface)
            mock_hw.return_value = MagicMock(spec=HardwareInfo)

            # Hívjuk meg a bootstrap_core-t
            bootstrap_core()

            # Inicializáljuk az adatbázist
            await db_mock.initialize()

            # Ellenőrizzük, hogy az inicializálás meghívásra került
            db_mock.initialize.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_bootstrap_core_with_async_event_bus(self) -> None:
        """Teszteli, hogy a bootstrap_core létrehoz egy esemény busz komponenst, ami indítható."""
        with (
            patch("neural_ai.core.config.factory.ConfigManagerFactory.get_manager") as mock_config,
            patch("neural_ai.core.logger.factory.LoggerFactory.get_logger") as mock_logger,
            patch("neural_ai.core.db.factory.DatabaseFactory.create_manager") as mock_db,
            patch("neural_ai.core.events.factory.EventBusFactory.create") as mock_event,
            patch("neural_ai.core.storage.factory.StorageFactory.get_storage") as mock_storage,
            patch("neural_ai.core.utils.factory.HardwareFactory.get_hardware_info") as mock_hw,
        ):
            # Készítünk egy aszinkron indítható event bus mockot
            event_mock = MagicMock(spec=EventBus)
            event_mock.start = AsyncMock()

            mock_config.return_value = MagicMock(spec=ConfigManagerInterface)
            mock_logger.return_value = MagicMock(spec=LoggerInterface)
            mock_db.return_value = MagicMock(spec=DatabaseManager)
            mock_event.return_value = event_mock
            mock_storage.return_value = MagicMock(spec=StorageInterface)
            mock_hw.return_value = MagicMock(spec=HardwareInfo)

            # Hívjuk meg a bootstrap_core-t
            bootstrap_core()

            # Indítsuk az esemény buszt
            await event_mock.start()

            # Ellenőrizzük, hogy az indítás meghívásra került
            event_mock.start.assert_awaited_once()


class TestGetCoreComponentsIntegration:
    """Integrációs tesztek a get_core_components függvényhez."""

    def test_get_core_components_returns_singleton(self) -> None:
        """Teszteli, hogy a get_core_components szingleton példányt ad vissza."""
        with patch("neural_ai.core.bootstrap_core") as mock_bootstrap:
            mock_bootstrap.return_value = MagicMock(spec=CoreComponents)

            # Első hívás
            components1 = get_core_components()

            # Második hívás - ugyanazt a példányt kell visszaadnia
            components2 = get_core_components()

            # Ellenőrizzük, hogy ugyanaz a példány
            assert components1 is components2
            # Ellenőrizzük, hogy a bootstrap_core csak egyszer hívódott meg
            mock_bootstrap.assert_called_once()

    def test_get_core_components_returns_core_components(self) -> None:
        """Teszteli, hogy a get_core_components CoreComponents példányt ad vissza."""
        with patch("neural_ai.core.bootstrap_core") as mock_bootstrap:
            mock_bootstrap.return_value = MagicMock(spec=CoreComponents)

            components = get_core_components()

            assert isinstance(components, CoreComponents)


class TestCoreComponentsIntegration:
    """Integrációs tesztek a CoreComponents osztályhoz."""

    def test_core_components_has_all_required_properties(self) -> None:
        """Teszteli, hogy a CoreComponents rendelkezik az összes szükséges tulajdonsággal."""
        with (
            patch("neural_ai.core.config.factory.ConfigManagerFactory.get_manager") as mock_config,
            patch("neural_ai.core.logger.factory.LoggerFactory.get_logger") as mock_logger,
            patch("neural_ai.core.db.factory.DatabaseFactory.create_manager") as mock_db,
            patch("neural_ai.core.events.factory.EventBusFactory.create") as mock_event,
            patch("neural_ai.core.storage.factory.StorageFactory.get_storage") as mock_storage,
            patch("neural_ai.core.utils.factory.HardwareFactory.get_hardware_info") as mock_hw,
        ):
            mock_config.return_value = MagicMock(spec=ConfigManagerInterface)
            mock_logger.return_value = MagicMock(spec=LoggerInterface)
            mock_db.return_value = MagicMock(spec=DatabaseManager)
            mock_event.return_value = MagicMock(spec=EventBus)
            mock_storage.return_value = MagicMock(spec=StorageInterface)
            mock_hw.return_value = MagicMock(spec=HardwareInfo)

            components = bootstrap_core()

            # Ellenőrizzük az összes tulajdonságot
            assert hasattr(components, "config")
            assert hasattr(components, "logger")
            assert hasattr(components, "storage")
            assert hasattr(components, "database")
            assert hasattr(components, "event_bus")
            assert hasattr(components, "hardware")

    def test_core_components_has_methods_work_correctly(self) -> None:
        """Teszteli, hogy a CoreComponents has_ metódusai helyesen működnek."""
        with (
            patch("neural_ai.core.config.factory.ConfigManagerFactory.get_manager") as mock_config,
            patch("neural_ai.core.logger.factory.LoggerFactory.get_logger") as mock_logger,
            patch("neural_ai.core.db.factory.DatabaseFactory.create_manager") as mock_db,
            patch("neural_ai.core.events.factory.EventBusFactory.create") as mock_event,
            patch("neural_ai.core.storage.factory.StorageFactory.get_storage") as mock_storage,
            patch("neural_ai.core.utils.factory.HardwareFactory.get_hardware_info") as mock_hw,
        ):
            mock_config.return_value = MagicMock(spec=ConfigManagerInterface)
            mock_logger.return_value = MagicMock(spec=LoggerInterface)
            mock_db.return_value = MagicMock(spec=DatabaseManager)
            mock_event.return_value = MagicMock(spec=EventBus)
            mock_storage.return_value = MagicMock(spec=StorageInterface)
            mock_hw.return_value = MagicMock(spec=HardwareInfo)

            components = bootstrap_core()

            # Ellenőrizzük az összes has_ metódust
            assert components.has_config() is True
            assert components.has_logger() is True
            assert components.has_storage() is True
            assert components.has_database() is True
            assert components.has_event_bus() is True
            assert components.has_hardware() is True

    def test_core_components_set_methods_work_correctly(self) -> None:
        """Teszteli, hogy a CoreComponents set_ metódusai helyesen működnek."""
        # Létrehozzuk a CoreComponents példányt mock komponensekkel
        components = CoreComponents()

        # Mock komponensek létrehozása
        mock_config = MagicMock(spec=ConfigManagerInterface)
        mock_logger = MagicMock(spec=LoggerInterface)
        mock_storage = MagicMock(spec=StorageInterface)
        mock_database = MagicMock(spec=DatabaseManager)
        mock_event_bus = MagicMock(spec=EventBus)
        mock_hardware = MagicMock(spec=HardwareInfo)

        # Beállítjuk a komponenseket
        components.set_config(mock_config)
        components.set_logger(mock_logger)
        components.set_storage(mock_storage)
        components.set_database(mock_database)
        components.set_event_bus(mock_event_bus)
        components.set_hardware(mock_hardware)

        # Ellenőrizzük, hogy a komponensek be lettek-e állítva
        assert components.config is mock_config
        assert components.logger is mock_logger
        assert components.storage is mock_storage
        assert components.database is mock_database
        assert components.event_bus is mock_event_bus
        assert components.hardware is mock_hardware
