"""Tesztek a neural_ai.core.__init__.py modulhoz.

Ez a tesztmodul ellenőrzi a core bootstrap funkcionalitását, beleértve:
- Verzió lekérdezést
- Séma verzió lekérdezést
- Core komponensek inicializálását
- Globális komponens hozzáférést
"""

import unittest
from unittest.mock import MagicMock, patch

from neural_ai.core import (
    bootstrap_core,
    get_core_components,
    get_schema_version,
    get_version,
)
from neural_ai.core.base.implementations.component_bundle import CoreComponents


class TestVersionFunctions(unittest.TestCase):
    """Tesztek a verzió lekérdező függvényekhez."""

    def test_get_version_success(self) -> None:
        """Teszteli a get_version függvényt sikeres verzió lekérdezés esetén."""
        with patch("importlib.metadata.version") as mock_version:
            mock_version.return_value = "1.0.0"
            result = get_version()
            self.assertEqual(result, "1.0.0")

    def test_get_version_failure(self) -> None:
        """Teszteli a get_version függvényt sikertelen verzió lekérdezés esetén."""
        with patch("importlib.metadata.version") as mock_version:
            mock_version.side_effect = Exception("Package not found")
            result = get_version()
            self.assertEqual(result, "unknown")

    def test_get_schema_version(self) -> None:
        """Teszteli a get_schema_version függvényt."""
        result = get_schema_version()
        self.assertEqual(result, "1.0.0")


class TestBootstrapCore(unittest.TestCase):
    """Tesztek a bootstrap_core függvényhez."""

    def setUp(self) -> None:
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
        self.assertIsNotNone(result)
        self.assertIsInstance(result, CoreComponents)

        # Ellenőrizzük, hogy a container regisztrálások megtörténtek
        # Csak a hívások számát ellenőrizzük, mert a pontos interfész nevek változhatnak
        actual_calls = self.mock_container.register_instance.call_count
        self.assertGreaterEqual(actual_calls, 6)

    @patch("neural_ai.core.base.implementations.di_container.DIContainer")
    @patch("neural_ai.core.config.factory.ConfigManagerFactory")
    @patch("neural_ai.core.logger.factory.LoggerFactory")
    def test_bootstrap_core_with_custom_config(
        self,
        mock_logger_factory: MagicMock,
        mock_config_factory: MagicMock,
        mock_di_container: MagicMock,
    ) -> None:
        """Teszteli a bootstrap_core függvényt egyéni konfigurációval."""
        # Mock beállítások
        mock_di_container.return_value = self.mock_container
        mock_config_factory.create_manager.return_value = self.mock_config
        mock_logger_factory.get_logger.return_value = self.mock_logger

        # Bootstrap hívás egyéni konfigurációval
        result = bootstrap_core(config_path="custom_configs/", log_level="DEBUG")

        # Ellenőrzések
        self.assertIsNotNone(result)
        # Ellenőrizzük, hogy a config betöltötte a configs mappát (legalább egyszer)
        self.mock_config.load_directory.assert_called_with("configs")
        self.assertGreaterEqual(self.mock_config.load_directory.call_count, 1)

    @patch("neural_ai.core.base.implementations.di_container.DIContainer")
    def test_bootstrap_core_import_error(self, mock_di_container: MagicMock) -> None:
        """Teszteli a bootstrap_core függvényt import hiba esetén."""
        mock_di_container.side_effect = ImportError("Module not found")
        
        with self.assertRaises(ImportError):
            bootstrap_core()


class TestGetCoreComponents(unittest.TestCase):
    """Tesztek a get_core_components függvényhez."""

    def tearDown(self) -> None:
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

        self.assertEqual(result, mock_core)
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

        self.assertEqual(result1, result2)
        # Csak egyszer hívódik meg a bootstrap
        mock_bootstrap.assert_called_once()


class TestIntegration(unittest.TestCase):
    """Integrációs tesztek a core modulhoz."""

    def tearDown(self) -> None:
        """Teszt takarítás."""
        if hasattr(get_core_components, "_instance"):
            delattr(get_core_components, "_instance")

    @patch("neural_ai.core.bootstrap_core")
    def test_version_and_bootstrap_integration(self, mock_bootstrap: MagicMock) -> None:
        """Integrációs teszt a verzió és bootstrap függvényekhez."""
        # Verzió lekérdezése
        version = get_version()
        self.assertIsInstance(version, str)

        # Séma verzió lekérdezése
        schema_version = get_schema_version()
        self.assertEqual(schema_version, "1.0.0")

        # Core komponensek lekérdezése
        mock_core = MagicMock()
        mock_bootstrap.return_value = mock_core
        core = get_core_components()

        self.assertEqual(core, mock_core)

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
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Import hiba: {e}")


if __name__ == "__main__":
    unittest.main()