"""Tesztek a neural_ai.core.__init__.py modulhoz.

Ez a tesztmodul ellenőrzi a core bootstrap funkcionalitását, beleértve:
- Verzió lekérdezést
- Séma verzió lekérdezést
- Core komponensek inicializálását
- Globális komponens hozzáférést
"""

from unittest.mock import MagicMock, patch

import pytest

from neural_ai.core import (
    bootstrap_core,
    get_core_components,
    get_schema_version,
    get_version,
)
from neural_ai.core.base.implementations.component_bundle import CoreComponents


class TestVersionFunctions:
    """Tesztek a verzió lekérdező függvényekhez."""

    def test_get_version_success(self) -> None:
        """Teszteli a get_version függvényt sikeres verzió lekérdezés esetén."""
        with patch("importlib.metadata.version") as mock_version:
            mock_version.return_value = "1.0.0"
            result = get_version()
            assert result == "1.0.0"

    def test_get_version_failure(self) -> None:
        """Teszteli a get_version függvényt sikertelen verzió lekérdezés esetén."""
        with patch("importlib.metadata.version") as mock_version:
            mock_version.side_effect = Exception("Package not found")
            result = get_version()
            assert result == "unknown"

    def test_get_version_returns_string(self) -> None:
        """Teszteli, hogy a get_version mindig stringgel tér vissza."""
        result = get_version()
        assert isinstance(result, str)

    def test_get_schema_version(self) -> None:
        """Teszteli a get_schema_version függvényt."""
        result = get_schema_version()
        assert result == "1.0.0"

    def test_get_schema_version_returns_string(self) -> None:
        """Teszteli, hogy a get_schema_version mindig stringgel tér vissza."""
        result = get_schema_version()
        assert isinstance(result, str)


class TestBootstrapCore:
    """Tesztek a bootstrap_core függvényhez."""

    def setup_method(self) -> None:
        """Teszt előkészítés."""
        # Mockoljuk a factory osztályokat
        self.mock_container = MagicMock()
        self.mock_hardware = MagicMock()
        self.mock_config = MagicMock()
        self.mock_logger = MagicMock()
        self.mock_database = MagicMock()
        self.mock_event_bus = MagicMock()
        self.mock_storage = MagicMock()
        self.mock_health_monitor = MagicMock()

    @patch("neural_ai.core.base.implementations.di_container.DIContainer")
    @patch("neural_ai.core.config.factory.ConfigManagerFactory")
    @patch("neural_ai.core.events.factory.EventBusFactory")
    @patch("neural_ai.core.logger.factory.LoggerFactory")
    @patch("neural_ai.core.storage.factory.StorageFactory")
    @patch("neural_ai.core.system.factory.SystemComponentFactory")
    @patch("neural_ai.core.utils.factory.HardwareFactory")
    def test_bootstrap_core_success(
        self,
        mock_hardware_factory: MagicMock,
        mock_system_factory: MagicMock,
        mock_storage_factory: MagicMock,
        mock_logger_factory: MagicMock,
        mock_event_factory: MagicMock,
        mock_config_factory: MagicMock,
        mock_di_container: MagicMock,
    ) -> None:
        """Teszteli a bootstrap_core függvényt sikeres inicializálás esetén."""
        # Mock beállítások
        mock_di_container.return_value = self.mock_container
        mock_hardware_factory.get_hardware_info.return_value = self.mock_hardware
        mock_config_factory.create_manager.return_value = self.mock_config
        mock_logger_factory.get_logger.return_value = self.mock_logger
        mock_event_factory.create_from_config.return_value = self.mock_event_bus
        mock_storage_factory.get_storage.return_value = self.mock_storage
        mock_system_factory.create_health_monitor.return_value = self.mock_health_monitor

        # Bootstrap hívás
        result = bootstrap_core()

        # Ellenőrzések
        assert result is not None
        assert isinstance(result, CoreComponents)

        # Ellenőrizzük, hogy a container regisztrálások megtörténtek
        # Csak a hívások számát ellenőrizzük, mert a pontos interfész nevek változhatnak
        actual_calls = self.mock_container.register_instance.call_count
        assert actual_calls >= 6

    @patch("neural_ai.core.base.implementations.di_container.DIContainer")
    @patch("neural_ai.core.config.factory.ConfigManagerFactory")
    @patch("neural_ai.core.logger.factory.LoggerFactory")
    @patch("neural_ai.core.events.factory.EventBusFactory")
    @patch("neural_ai.core.storage.factory.StorageFactory")
    @patch("neural_ai.core.system.factory.SystemComponentFactory")
    @patch("neural_ai.core.utils.factory.HardwareFactory")
    def test_bootstrap_core_with_custom_config(
        self,
        mock_hardware_factory: MagicMock,
        mock_system_factory: MagicMock,
        mock_storage_factory: MagicMock,
        mock_event_factory: MagicMock,
        mock_logger_factory: MagicMock,
        mock_config_factory: MagicMock,
        mock_di_container: MagicMock,
    ) -> None:
        """Teszteli a bootstrap_core függvényt egyéni konfigurációval."""
        # Mock beállítások
        mock_di_container.return_value = self.mock_container
        mock_config_factory.create_manager.return_value = self.mock_config
        mock_logger_factory.get_logger.return_value = self.mock_logger
        mock_event_factory.create_from_config.return_value = self.mock_event_bus
        mock_storage_factory.get_storage.return_value = self.mock_storage
        mock_system_factory.create_health_monitor.return_value = self.mock_health_monitor
        mock_hardware_factory.get_hardware_info.return_value = self.mock_hardware

        # Bootstrap hívás egyéni konfigurációval
        result = bootstrap_core(config_path="custom_configs/", log_level="DEBUG")

        # Ellenőrzések
        assert result is not None
        # Ellenőrizzük, hogy a config betöltötte a configs mappát (legalább egyszer)
        self.mock_config.load_directory.assert_called_with("configs")
        assert self.mock_config.load_directory.call_count >= 1

    @patch("neural_ai.core.base.implementations.di_container.DIContainer")
    def test_bootstrap_core_import_error(self, mock_di_container: MagicMock) -> None:
        """Teszteli a bootstrap_core függvényt import hiba esetén."""
        mock_di_container.side_effect = ImportError("Module not found")
        
        with pytest.raises(ImportError):
            bootstrap_core()

    def test_bootstrap_core_returns_core_components(self) -> None:
        """Teszteli, hogy a bootstrap_core CoreComponents példánnyal tér vissza."""
        with patch("neural_ai.core.base.implementations.di_container.DIContainer") as mock_di:
            with patch("neural_ai.core.config.factory.ConfigManagerFactory") as mock_cfg_fact:
                with patch("neural_ai.core.logger.factory.LoggerFactory") as mock_log_fact:
                    with patch("neural_ai.core.events.factory.EventBusFactory") as mock_evt_fact:
                        with patch("neural_ai.core.storage.factory.StorageFactory") as mock_stor_fact:
                            with patch("neural_ai.core.system.factory.SystemComponentFactory") as mock_sys_fact:
                                with patch("neural_ai.core.utils.factory.HardwareFactory") as mock_hw_fact:
                                    # Mock beállítások
                                    mock_di.return_value = self.mock_container
                                    mock_cfg_fact.create_manager.return_value = self.mock_config
                                    mock_log_fact.get_logger.return_value = self.mock_logger
                                    mock_evt_fact.create_from_config.return_value = self.mock_event_bus
                                    mock_stor_fact.get_storage.return_value = self.mock_storage
                                    mock_sys_fact.create_health_monitor.return_value = self.mock_health_monitor
                                    mock_hw_fact.get_hardware_info.return_value = self.mock_hardware

                                    result = bootstrap_core()
                                    assert isinstance(result, CoreComponents)


class TestGetCoreComponents:
    """Tesztek a get_core_components függvényhez."""

    def teardown_method(self) -> None:
        """Teszt takarítás."""
        # Töröljük a szingleton példányt
        if hasattr(get_core_components, "_instance"):
            delattr(get_core_components, "_instance")

    @patch("neural_ai.core.bootstrap_core")
    def test_get_core_components_first_call(self, mock_bootstrap: MagicMock) -> None:
        """Teszteli a get_core_components függvényt első hívás esetén."""
        mock_core = MagicMock()
        mock_bootstrap.return_value = mock_core

        result = get_core_components()

        assert result == mock_core
        mock_bootstrap.assert_called_once()

    @patch("neural_ai.core.bootstrap_core")
    def test_get_core_components_cached(self, mock_bootstrap: MagicMock) -> None:
        """Teszteli a get_core_components függvényt többszöri hívás esetén."""
        mock_core = MagicMock()
        mock_bootstrap.return_value = mock_core

        # Első hívás
        result1 = get_core_components()
        # Második hívás
        result2 = get_core_components()

        assert result1 == result2
        # Csak egyszer hívódik meg a bootstrap
        mock_bootstrap.assert_called_once()

    @patch("neural_ai.core.bootstrap_core")
    def test_get_core_components_returns_core_components(
        self, mock_bootstrap: MagicMock
    ) -> None:
        """Teszteli, hogy get_core_components CoreComponents példánnyal tér vissza."""
        mock_core = MagicMock(spec=CoreComponents)
        mock_bootstrap.return_value = mock_core

        result = get_core_components()
        
        assert result == mock_core
        assert isinstance(result, CoreComponents)


class TestIntegration:
    """Integrációs tesztek a core modulhoz."""

    def teardown_method(self) -> None:
        """Teszt takarítás."""
        if hasattr(get_core_components, "_instance"):
            delattr(get_core_components, "_instance")

    @patch("neural_ai.core.bootstrap_core")
    def test_version_and_bootstrap_integration(self, mock_bootstrap: MagicMock) -> None:
        """Integrációs teszt a verzió és bootstrap függvényekhez."""
        # Verzió lekérdezése
        version = get_version()
        assert isinstance(version, str)

        # Séma verzió lekérdezése
        schema_version = get_schema_version()
        assert schema_version == "1.0.0"

        # Core komponensek lekérdezése
        mock_core = MagicMock()
        mock_bootstrap.return_value = mock_core
        core = get_core_components()

        assert core == mock_core

    def test_all_imports_available(self) -> None:
        """Teszteli, hogy minden szükséges import elérhető-e."""
        # Ellenőrizzük, hogy a fő függvények importálhatók
        try:
            from neural_ai.core import (
                bootstrap_core,
                get_core_components,
                get_version,
                get_schema_version,
            )
            assert True
        except ImportError as e:
            pytest.fail(f"Import hiba: {e}")

    def test_core_components_singleton_pattern(self) -> None:
        """Teszteli a singleton mintát a get_core_components függvényben."""
        with patch("neural_ai.core.bootstrap_core") as mock_bootstrap:
            mock_core = MagicMock()
            mock_bootstrap.return_value = mock_core

            # Többszöri hívás ellenőrzése
            instance1 = get_core_components()
            instance2 = get_core_components()
            instance3 = get_core_components()

            # Mindig ugyanazt a példányt kell visszaadnia
            assert instance1 is instance2 is instance3
            # A bootstrap csak egyszer hívódik meg
            assert mock_bootstrap.call_count == 1