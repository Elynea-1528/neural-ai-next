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
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
from neural_ai.core.storage.interfaces.storage_interface import StorageInterface


class TestCoreComponents:
    """CoreComponents osztály tesztjei."""

    def test_core_components_initialization(self) -> None:
        """Teszteli a CoreComponents inicializálását."""
        # Mock objektumok létrehozása
        mock_config = Mock(spec=ConfigManagerInterface)
        mock_logger = Mock(spec=LoggerInterface)
        mock_storage = Mock(spec=StorageInterface)

        # CoreComponents létrehozása
        components = CoreComponents(config=mock_config, logger=mock_logger, storage=mock_storage)

        # Ellenőrzések
        assert components.config is mock_config
        assert components.logger is mock_logger
        assert components.storage is mock_storage

    def test_core_components_type_hints(self) -> None:
        """Teszteli a CoreComponents típushelyességét."""
        mock_config = Mock(spec=ConfigManagerInterface)
        mock_logger = Mock(spec=LoggerInterface)
        mock_storage = Mock(spec=StorageInterface)

        components = CoreComponents(config=mock_config, logger=mock_logger, storage=mock_storage)

        # Típus ellenőrzések
        assert isinstance(components.config, ConfigManagerInterface)
        assert isinstance(components.logger, LoggerInterface)
        assert isinstance(components.storage, StorageInterface)

    def test_core_components_attributes(self) -> None:
        """Teszteli a CoreComponents attribútumait."""
        mock_config = Mock(spec=ConfigManagerInterface)
        mock_logger = Mock(spec=LoggerInterface)
        mock_storage = Mock(spec=StorageInterface)

        components = CoreComponents(config=mock_config, logger=mock_logger, storage=mock_storage)

        # Attribútumok ellenőrzése
        assert hasattr(components, "config")
        assert hasattr(components, "logger")
        assert hasattr(components, "storage")


class TestBootstrapCore:
    """Bootstrap funkció tesztjei."""

    @patch("neural_ai.core.config.implementations.config_manager_factory.ConfigManagerFactory")
    @patch("neural_ai.core.logger.implementations.logger_factory.LoggerFactory")
    @patch("neural_ai.core.storage.implementations.storage_factory.StorageFactory")
    def test_bootstrap_core_default(
        self, mock_storage_factory: Mock, mock_logger_factory: Mock, mock_config_factory: Mock
    ) -> None:
        """Teszteli a bootstrap_core alapértelmezett működését."""
        # Mock objektumok beállítása
        mock_config = Mock(spec=ConfigManagerInterface)
        mock_logger = Mock(spec=LoggerInterface)
        mock_storage = Mock(spec=StorageInterface)

        mock_config_factory.get_manager.return_value = mock_config
        mock_logger_factory.get_logger.return_value = mock_logger
        mock_storage_factory.get_storage.return_value = mock_storage

        # Bootstrap futtatása
        core = bootstrap_core()

        # Ellenőrzések
        assert isinstance(core, CoreComponents)
        assert core.config is mock_config
        assert core.logger is mock_logger
        assert core.storage is mock_storage

        # Factory hívások ellenőrzése
        mock_config_factory.get_manager.assert_called_once_with(filename="config.yml")
        mock_logger_factory.get_logger.assert_called_once_with(
            name="NeuralAI", logger_type="default", level=None
        )
        mock_storage_factory.get_storage.assert_called_once_with(
            storage_type="file", base_path=None, logger=mock_logger
        )

    @patch("neural_ai.core.config.implementations.config_manager_factory.ConfigManagerFactory")
    @patch("neural_ai.core.logger.implementations.logger_factory.LoggerFactory")
    @patch("neural_ai.core.storage.implementations.storage_factory.StorageFactory")
    def test_bootstrap_core_with_parameters(
        self, mock_storage_factory: Mock, mock_logger_factory: Mock, mock_config_factory: Mock
    ) -> None:
        """Teszteli a bootstrap_core paraméterezését."""
        # Mock objektumok
        mock_config = Mock(spec=ConfigManagerInterface)
        mock_logger = Mock(spec=LoggerInterface)
        mock_storage = Mock(spec=StorageInterface)

        mock_config_factory.get_manager.return_value = mock_config
        mock_logger_factory.get_logger.return_value = mock_logger
        mock_storage_factory.get_storage.return_value = mock_storage

        # Bootstrap futtatása paraméterekkel
        config_path = "/path/to/config.yaml"
        log_level = "DEBUG"
        core = bootstrap_core(config_path=config_path, log_level=log_level)

        # Ellenőrzések
        assert isinstance(core, CoreComponents)

        # Factory hívások ellenőrzése paraméterekkel
        mock_config_factory.get_manager.assert_called_once_with(filename=config_path)
        mock_logger_factory.get_logger.assert_called_once_with(
            name="NeuralAI", logger_type="default", level=log_level
        )

    def test_bootstrap_core_returns_core_components(self) -> None:
        """Teszteli, hogy a bootstrap_core CoreComponents-t ad-e vissza."""
        with (
            patch(
                "neural_ai.core.config.implementations.config_manager_factory.ConfigManagerFactory"
            ) as mock_cf,
            patch("neural_ai.core.logger.implementations.logger_factory.LoggerFactory") as mock_lf,
            patch(
                "neural_ai.core.storage.implementations.storage_factory.StorageFactory"
            ) as mock_sf,
        ):
            mock_cf.get_manager.return_value = Mock(spec=ConfigManagerInterface)
            mock_lf.get_logger.return_value = Mock(spec=LoggerInterface)
            mock_sf.get_storage.return_value = Mock(spec=StorageInterface)
            mock_lf.create_logger.return_value = Mock(spec=LoggerInterface)
            mock_sf.create_storage.return_value = Mock(spec=StorageInterface)

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
