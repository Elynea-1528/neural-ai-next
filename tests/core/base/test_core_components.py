"""Core komponensek tesztjei."""

import unittest
from unittest.mock import MagicMock, patch
from typing import Any

from neural_ai.core.base.container import DIContainer
from neural_ai.core.base.core_components import CoreComponents, LazyLoader


class TestLazyLoader(unittest.TestCase):
    """LazyLoader osztály tesztjei."""

    def test_lazy_loader_initialization(self) -> None:
        """Teszteli a LazyLoader inicializálását."""
        def loader_func() -> str:
            return "loaded_value"

        loader = LazyLoader(loader_func)
        self.assertFalse(loader.is_loaded)

    def test_lazy_loader_call(self) -> None:
        """Teszteli a LazyLoader hívását."""
        def loader_func() -> str:
            return "loaded_value"

        loader = LazyLoader(loader_func)
        result = loader()

        self.assertEqual(result, "loaded_value")
        self.assertTrue(loader.is_loaded)

    def test_lazy_loader_reset(self) -> None:
        """Teszteli a LazyLoader resetelését."""
        def loader_func() -> str:
            return "loaded_value"

        loader = LazyLoader(loader_func)
        loader()

        self.assertTrue(loader.is_loaded)
        loader.reset()
        self.assertFalse(loader.is_loaded)


class TestCoreComponents(unittest.TestCase):
    """CoreComponents osztály tesztjei."""

    def setUp(self) -> None:
        """Teszt előkészítése."""
        self.container = DIContainer()
        self.core_components = CoreComponents(container=self.container)

    def test_core_components_initialization_with_container(self) -> None:
        """Teszteli a CoreComponents inicializálását konténerrel."""
        self.assertTrue(hasattr(self.core_components, '_container'))
        self.assertTrue(hasattr(self.core_components, '_factory'))

    def test_core_components_initialization_without_container(self) -> None:
        """Teszteli a CoreComponents inicializálását konténer nélkül."""
        components = CoreComponents()
        self.assertTrue(hasattr(components, '_container'))

    def test_config_property_with_registered_component(self) -> None:
        """Teszteli a config property-t regisztrált komponenssel."""
        from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
        mock_config = MagicMock(spec=ConfigManagerInterface)
        self.container.register_instance(ConfigManagerInterface, mock_config)

        result = self.core_components.config
        self.assertEqual(result, mock_config)

    def test_config_property_without_registered_component(self) -> None:
        """Teszteli a config property-t regisztrált komponens nélkül."""
        result = self.core_components.config
        self.assertIsNone(result)

    def test_logger_property_with_registered_component(self) -> None:
        """Teszteli a logger property-t regisztrált komponenssel."""
        from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
        mock_logger = MagicMock(spec=LoggerInterface)
        self.container.register_instance(LoggerInterface, mock_logger)

        result = self.core_components.logger
        self.assertEqual(result, mock_logger)

    def test_logger_property_without_registered_component(self) -> None:
        """Teszteli a logger property-t regisztrált komponens nélkül."""
        result = self.core_components.logger
        self.assertIsNone(result)

    def test_storage_property_with_registered_component(self) -> None:
        """Teszteli a storage property-t regisztrált komponenssel."""
        from neural_ai.core.storage.interfaces.storage_interface import StorageInterface
        mock_storage = MagicMock(spec=StorageInterface)
        self.container.register_instance(StorageInterface, mock_storage)

        result = self.core_components.storage
        self.assertEqual(result, mock_storage)

    def test_storage_property_without_registered_component(self) -> None:
        """Teszteli a storage property-t regisztrált komponens nélkül."""
        result = self.core_components.storage
        self.assertIsNone(result)

    @patch('neural_ai.core.base.core_components.ConfigManagerInterface')
    def test_set_config(self, MockConfig: Any) -> None:
        """Teszteli a set_config metódust."""
        mock_config = MockConfig()
        self.core_components.set_config(mock_config)

        result = self.core_components.config
        self.assertEqual(result, mock_config)

    @patch('neural_ai.core.base.core_components.LoggerInterface')
    def test_set_logger(self, MockLogger: Any) -> None:
        """Teszteli a set_logger metódust."""
        mock_logger = MockLogger()
        self.core_components.set_logger(mock_logger)

        result = self.core_components.logger
        self.assertEqual(result, mock_logger)

    @patch('neural_ai.core.base.core_components.StorageInterface')
    def test_set_storage(self, MockStorage: Any) -> None:
        """Teszteli a set_storage metódust."""
        mock_storage = MockStorage()
        self.core_components.set_storage(mock_storage)

        result = self.core_components.storage
        self.assertEqual(result, mock_storage)

    def test_has_config_without_component(self) -> None:
        """Teszteli a has_config metódust komponens nélkül."""
        result = self.core_components.has_config()
        self.assertFalse(result)

    @patch('neural_ai.core.base.core_components.ConfigManagerInterface')
    def test_has_config_with_component(self, MockConfig: Any) -> None:
        """Teszteli a has_config metódust komponenssel."""
        mock_config = MockConfig()
        self.core_components.set_config(mock_config)

        result = self.core_components.has_config()
        self.assertTrue(result)

    def test_has_logger_without_component(self) -> None:
        """Teszteli a has_logger metódust komponens nélkül."""
        result = self.core_components.has_logger()
        self.assertFalse(result)

    @patch('neural_ai.core.base.core_components.LoggerInterface')
    def test_has_logger_with_component(self, MockLogger: Any) -> None:
        """Teszteli a has_logger metódust komponenssel."""
        mock_logger = MockLogger()
        self.core_components.set_logger(mock_logger)

        result = self.core_components.has_logger()
        self.assertTrue(result)

    def test_has_storage_without_component(self) -> None:
        """Teszteli a has_storage metódust komponens nélkül."""
        result = self.core_components.has_storage()
        self.assertFalse(result)

    @patch('neural_ai.core.base.core_components.StorageInterface')
    def test_has_storage_with_component(self, MockStorage: Any) -> None:
        """Teszteli a has_storage metódust komponenssel."""
        mock_storage = MockStorage()
        self.core_components.set_storage(mock_storage)

        result = self.core_components.has_storage()
        self.assertTrue(result)

    def test_validate_without_components(self) -> None:
        """Teszteli a validate metódust komponensek nélkül."""
        result = self.core_components.validate()
        self.assertFalse(result)

    @patch('neural_ai.core.base.core_components.ConfigManagerInterface')
    @patch('neural_ai.core.base.core_components.LoggerInterface')
    @patch('neural_ai.core.base.core_components.StorageInterface')
    def test_validate_with_all_components(
        self,
        MockConfig: Any,
        MockLogger: Any,
        MockStorage: Any
    ) -> None:
        """Teszteli a validate metódust minden komponenssel."""
        mock_config = MockConfig()
        mock_logger = MockLogger()
        mock_storage = MockStorage()

        self.core_components.set_config(mock_config)
        self.core_components.set_logger(mock_logger)
        self.core_components.set_storage(mock_storage)

        result = self.core_components.validate()
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()