"""Core modul inicializációs tesztjei.

Ez a tesztmodul ellenőrzi a neural_ai.core.__init__ modul
megfelelő működését, függőségi injektálását és inicializálását.
"""

from unittest.mock import Mock, patch

from neural_ai.core import (
    CoreComponents,
    bootstrap_core,
    get_core_components,
    get_schema_version,
    get_version,
)
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.db.implementations.sqlalchemy_session import DatabaseManager
from neural_ai.core.events.implementations.zeromq_bus import EventBus
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
from neural_ai.core.storage.interfaces.storage_interface import StorageInterface
from neural_ai.core.utils.implementations.hardware_info import HardwareInfo


class TestCoreComponents:
    """CoreComponents osztály tesztjei."""

    def test_core_components_initialization(self) -> None:
        """Teszteli a CoreComponents inicializálását."""
        # Mock objektumok létrehozása
        mock_config = Mock(spec=ConfigManagerInterface)
        mock_logger = Mock(spec=LoggerInterface)
        mock_storage = Mock(spec=StorageInterface)
        mock_database = Mock(spec=DatabaseManager)
        mock_event_bus = Mock(spec=EventBus)
        mock_hardware = Mock(spec=HardwareInfo)

        # CoreComponents létrehozása
        components = CoreComponents(
            config=mock_config,
            logger=mock_logger,
            storage=mock_storage,
            database=mock_database,
            event_bus=mock_event_bus,
            hardware=mock_hardware,
        )

        # Ellenőrzések
        assert components.config is mock_config
        assert components.logger is mock_logger
        assert components.storage is mock_storage
        assert components.database is mock_database
        assert components.event_bus is mock_event_bus
        assert components.hardware is mock_hardware

    def test_core_components_type_hints(self) -> None:
        """Teszteli a CoreComponents típushelyességét."""
        mock_config = Mock(spec=ConfigManagerInterface)
        mock_logger = Mock(spec=LoggerInterface)
        mock_storage = Mock(spec=StorageInterface)
        mock_database = Mock(spec=DatabaseManager)
        mock_event_bus = Mock(spec=EventBus)
        mock_hardware = Mock(spec=HardwareInfo)

        components = CoreComponents(
            config=mock_config,
            logger=mock_logger,
            storage=mock_storage,
            database=mock_database,
            event_bus=mock_event_bus,
            hardware=mock_hardware,
        )

        # Típus ellenőrzések
        assert isinstance(components.config, ConfigManagerInterface)
        assert isinstance(components.logger, LoggerInterface)
        assert isinstance(components.storage, StorageInterface)
        assert isinstance(components.database, DatabaseManager)
        assert isinstance(components.event_bus, EventBus)
        assert isinstance(components.hardware, HardwareInfo)

    def test_core_components_attributes(self) -> None:
        """Teszteli a CoreComponents attribútumait."""
        mock_config = Mock(spec=ConfigManagerInterface)
        mock_logger = Mock(spec=LoggerInterface)
        mock_storage = Mock(spec=StorageInterface)
        mock_database = Mock(spec=DatabaseManager)
        mock_event_bus = Mock(spec=EventBus)
        mock_hardware = Mock(spec=HardwareInfo)

        components = CoreComponents(
            config=mock_config,
            logger=mock_logger,
            storage=mock_storage,
            database=mock_database,
            event_bus=mock_event_bus,
            hardware=mock_hardware,
        )

        # Attribútumok ellenőrzése
        assert hasattr(components, "config")
        assert hasattr(components, "logger")
        assert hasattr(components, "storage")
        assert hasattr(components, "database")
        assert hasattr(components, "event_bus")
        assert hasattr(components, "hardware")


class TestBootstrapCore:
    """Bootstrap funkció tesztjei."""

    @patch("neural_ai.core.utils.factory.HardwareFactory")
    @patch("neural_ai.core.db.factory.DatabaseFactory")
    @patch("neural_ai.core.events.factory.EventBusFactory")
    @patch("neural_ai.core.config.factory.ConfigManagerFactory")
    @patch("neural_ai.core.logger.factory.LoggerFactory")
    @patch("neural_ai.core.storage.factory.StorageFactory")
    def test_bootstrap_core_default(
        self, mock_storage_factory: Mock, mock_logger_factory: Mock, mock_config_factory: Mock,
        mock_event_bus_factory: Mock, mock_database_factory: Mock, mock_hardware_factory: Mock
    ) -> None:
        """Teszteli a bootstrap_core alapértelmezett működését."""
        # Mock objektumok beállítása
        mock_config = Mock(spec=ConfigManagerInterface)
        mock_logger = Mock(spec=LoggerInterface)
        mock_storage = Mock(spec=StorageInterface)
        mock_database = Mock(spec=DatabaseManager)
        mock_event_bus = Mock(spec=EventBus)
        mock_hardware = Mock(spec=HardwareInfo)

        mock_hardware_factory.get_hardware_info.return_value = mock_hardware
        mock_config_factory.get_manager.return_value = mock_config
        mock_logger_factory.get_logger.return_value = mock_logger
        mock_database_factory.create_manager.return_value = mock_database
        mock_event_bus_factory.create.return_value = mock_event_bus
        mock_storage_factory.get_storage.return_value = mock_storage

        # Bootstrap futtatása
        core = bootstrap_core()

        # Ellenőrzések
        assert isinstance(core, CoreComponents)
        assert core.config is mock_config
        assert core.logger is mock_logger
        assert core.storage is mock_storage
        assert core.database is mock_database
        assert core.event_bus is mock_event_bus
        assert core.hardware is mock_hardware

        # Factory hívások ellenőrzése
        mock_hardware_factory.get_hardware_info.assert_called_once()
        mock_config_factory.get_manager.assert_called_once_with(filename="config.yml")
        mock_logger_factory.get_logger.assert_called_once_with(
            name="NeuralAI", logger_type="default", level=None
        )
        mock_database_factory.create_manager.assert_called_once_with(config_manager=mock_config)
        mock_event_bus_factory.create.assert_called_once()
        mock_storage_factory.get_storage.assert_called_once_with(
            storage_type="file", base_path=None, logger=mock_logger
        )

    @patch("neural_ai.core.utils.factory.HardwareFactory")
    @patch("neural_ai.core.db.factory.DatabaseFactory")
    @patch("neural_ai.core.events.factory.EventBusFactory")
    @patch("neural_ai.core.config.factory.ConfigManagerFactory")
    @patch("neural_ai.core.logger.factory.LoggerFactory")
    @patch("neural_ai.core.storage.factory.StorageFactory")
    def test_bootstrap_core_with_parameters(
        self, mock_storage_factory: Mock, mock_logger_factory: Mock, mock_config_factory: Mock,
        mock_event_bus_factory: Mock, mock_database_factory: Mock, mock_hardware_factory: Mock
    ) -> None:
        """Teszteli a bootstrap_core paraméterezését."""
        # Mock objektumok
        mock_config = Mock(spec=ConfigManagerInterface)
        mock_logger = Mock(spec=LoggerInterface)
        mock_storage = Mock(spec=StorageInterface)
        mock_database = Mock(spec=DatabaseManager)
        mock_event_bus = Mock(spec=EventBus)
        mock_hardware = Mock(spec=HardwareInfo)

        mock_hardware_factory.get_hardware_info.return_value = mock_hardware
        mock_config_factory.get_manager.return_value = mock_config
        mock_logger_factory.get_logger.return_value = mock_logger
        mock_database_factory.create_manager.return_value = mock_database
        mock_event_bus_factory.create.return_value = mock_event_bus
        mock_storage_factory.get_storage.return_value = mock_storage

        # Bootstrap futtatása paraméterekkel
        config_path = "/path/to/config.yaml"
        log_level = "DEBUG"
        core = bootstrap_core(config_path=config_path, log_level=log_level)

        # Ellenőrzések
        assert isinstance(core, CoreComponents)

        # Factory hívások ellenőrzése paraméterekkel
        mock_hardware_factory.get_hardware_info.assert_called_once()
        mock_config_factory.get_manager.assert_called_once_with(filename=config_path)
        mock_logger_factory.get_logger.assert_called_once_with(
            name="NeuralAI", logger_type="default", level=log_level
        )
        mock_database_factory.create_manager.assert_called_once_with(config_manager=mock_config)
        mock_event_bus_factory.create.assert_called_once()
        mock_storage_factory.get_storage.assert_called_once_with(
            storage_type="file", base_path=None, logger=mock_logger
        )

    def test_bootstrap_core_returns_core_components(self) -> None:
        """Teszteli, hogy a bootstrap_core CoreComponents-t ad-e vissza."""
        with (
            patch("neural_ai.core.utils.factory.HardwareFactory") as mock_hf,
            patch("neural_ai.core.db.factory.DatabaseFactory") as mock_df,
            patch("neural_ai.core.events.factory.EventBusFactory") as mock_ebf,
            patch("neural_ai.core.config.factory.ConfigManagerFactory") as mock_cf,
            patch("neural_ai.core.logger.factory.LoggerFactory") as mock_lf,
            patch("neural_ai.core.storage.factory.StorageFactory") as mock_sf,
        ):
            mock_hf.get_hardware_info.return_value = Mock(spec=HardwareInfo)
            mock_cf.get_manager.return_value = Mock(spec=ConfigManagerInterface)
            mock_lf.get_logger.return_value = Mock(spec=LoggerInterface)
            mock_df.create_manager.return_value = Mock(spec=DatabaseManager)
            mock_ebf.create.return_value = Mock(spec=EventBus)
            mock_sf.get_storage.return_value = Mock(spec=StorageInterface)

            core = bootstrap_core()
            assert isinstance(core, CoreComponents)


class TestGetCoreComponents:
    """get_core_components funkció tesztjei."""

    def test_get_core_components_singleton(self) -> None:
        """Teszteli a get_core_components szingleton viselkedését."""
        # Először töröljük a létező példányt
        if hasattr(get_core_components, "_instance"):
            delattr(get_core_components, "_instance")

        with patch("neural_ai.core.bootstrap_core") as mock_bootstrap:
            mock_bootstrap.return_value = Mock(spec=CoreComponents)

            # Első hívás
            core1 = get_core_components()
            assert core1 is not None
            assert isinstance(core1, CoreComponents)

            # Második hívás - ugyanazt a példányt kell visszaadnia
            core2 = get_core_components()
            assert core2 is core1

            # A bootstrap csak egyszer hívódott meg
            mock_bootstrap.assert_called_once()

    def test_get_core_components_returns_core_components(self) -> None:
        """Teszteli, hogy get_core_components CoreComponents-t ad-e vissza."""
        # Töröljük a létező példányt
        if hasattr(get_core_components, "_instance"):
            delattr(get_core_components, "_instance")

        with patch("neural_ai.core.bootstrap_core") as mock_bootstrap:
            mock_bootstrap.return_value = Mock(spec=CoreComponents)

            core = get_core_components()
            assert isinstance(core, CoreComponents)


class TestModuleExports:
    """Modul exportok tesztjei."""

    def test_module_all_export(self) -> None:
        """Teszteli a modul __all__ exportjait."""
        from neural_ai.core import __all__ as core_all

        expected_exports = [
            "CoreComponents",
            "bootstrap_core",
            "get_core_components",
            "get_version",
            "get_schema_version",
        ]

        for export in expected_exports:
            assert export in core_all

    def test_import_core_components(self) -> None:
        """Teszteli a CoreComponents importálhatóságát."""
        from neural_ai.core import CoreComponents

        assert CoreComponents is not None

    def test_import_bootstrap_core(self) -> None:
        """Teszteli a bootstrap_core importálhatóságát."""
        from neural_ai.core import bootstrap_core

        assert callable(bootstrap_core)

    def test_import_get_core_components(self) -> None:
        """Teszteli a get_core_components importálhatóságát."""
        from neural_ai.core import get_core_components

        assert callable(get_core_components)

    def test_import_get_version(self) -> None:
        """Teszteli a get_version importálhatóságát."""
        assert callable(get_version)

    def test_import_get_schema_version(self) -> None:
        """Teszteli a get_schema_version importálhatóságát."""
        assert callable(get_schema_version)


class TestVersionFunctions:
    """Verzió függvények tesztjei."""

    def test_get_version_returns_string(self) -> None:
        """Teszteli, hogy get_version stringgel tér-e vissza."""
        version = get_version()
        assert isinstance(version, str)

    def test_get_version_format(self) -> None:
        """Teszteli a get_version formátumát."""
        version = get_version()
        # A verzió vagy "unknown" vagy semver formátumú
        if version != "unknown":
            # Ellenőrizzük, hogy tartalmaz-e legalább egy pontot
            assert "." in version or version == "unknown"

    @patch("importlib.metadata.version")
    def test_get_version_returns_unknown_on_exception(self, mock_version: Mock) -> None:
        """Teszteli, hogy get_version 'unknown'-t ad vissza kivétel esetén."""
        # Mock kivétel dobása
        mock_version.side_effect = Exception("Package not found")

        version = get_version()
        assert version == "unknown"

    def test_get_schema_version_returns_string(self) -> None:
        """Teszteli, hogy get_schema_version stringgel tér-e vissza."""
        schema_version = get_schema_version()
        assert isinstance(schema_version, str)

    def test_get_schema_version_value(self) -> None:
        """Teszteli a get_schema_version értékét."""
        schema_version = get_schema_version()
        assert schema_version == "1.0.0"

    def test_get_schema_version_format(self) -> None:
        """Teszteli a get_schema_version formátumát."""
        schema_version = get_schema_version()
        # Séma verziónak semver formátumúnak kell lennie
        assert schema_version.count(".") == 2
        parts = schema_version.split(".")
        assert len(parts) == 3
        for part in parts:
            assert part.isdigit()
