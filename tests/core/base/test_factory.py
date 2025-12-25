"""Tesztek a CoreComponentFactory osztályhoz."""

from typing import Any
from unittest import mock

import pytest

from neural_ai.core.base.exceptions import ConfigurationError
from neural_ai.core.base.factory import CoreComponentFactory
from neural_ai.core.base.implementations.di_container import DIContainer
from neural_ai.core.base.implementations.lazy_loader import LazyLoader


class TestCoreComponentFactory:
    """CoreComponentFactory tesztelése."""

    def test_initialization(self) -> None:
        """Teszteli a factory inicializálását."""
        # Arrange
        container = DIContainer()

        # Act
        factory = CoreComponentFactory(container)

        # Assert
        assert factory._container is not None
        assert isinstance(factory._logger_loader, LazyLoader)
        assert isinstance(factory._config_loader, LazyLoader)
        assert isinstance(factory._storage_loader, LazyLoader)

    def test_reset_lazy_loaders(self) -> None:
        """Teszteli a lazy loader-ek visszaállítását."""
        # Arrange
        container = DIContainer()
        factory = CoreComponentFactory(container)

        # Először aktiváljuk a loader-eket
        factory._logger_loader._loaded = True
        factory._config_loader._loaded = True
        factory._storage_loader._loaded = True

        # Act
        factory.reset_lazy_loaders()

        # Assert
        assert not factory._logger_loader._loaded
        assert not factory._config_loader._loaded
        assert not factory._storage_loader._loaded

    def test_validate_dependencies_storage_missing_base_directory(self) -> None:
        """Teszteli a storage függőség ellenőrzését hiányzó base_directory esetén."""
        # Arrange
        config: dict[str, Any] = {}

        # Act & Assert
        with pytest.raises(ConfigurationError, match="Storage base_directory not configured"):
            CoreComponentFactory._validate_dependencies("storage", config)

    def test_validate_dependencies_storage_invalid_path(self) -> None:
        """Teszteli a storage függőség ellenőrzését érvénytelen útvonal esetén."""
        # Arrange
        config = {"base_directory": "/nonexistent/path/to/nowhere"}

        # Act & Assert
        with pytest.raises(ConfigurationError, match="Storage base_directory parent does not exist"):
            CoreComponentFactory._validate_dependencies("storage", config)

    def test_validate_dependencies_logger_missing_name(self) -> None:
        """Teszteli a logger függőség ellenőrzését hiányzó név esetén."""
        # Arrange
        config: dict[str, Any] = {}

        # Act & Assert
        with pytest.raises(ConfigurationError, match="Logger name not configured"):
            CoreComponentFactory._validate_dependencies("logger", config)

    def test_validate_dependencies_config_manager_missing_path(self) -> None:
        """Teszteli a config manager függőség ellenőrzését hiányzó fájlútvonal esetén."""
        # Arrange
        config: dict[str, Any] = {}

        # Act & Assert
        with pytest.raises(ConfigurationError, match="Config file path not configured"):
            CoreComponentFactory._validate_dependencies("config_manager", config)

    def test_validate_dependencies_config_manager_nonexistent_file(self) -> None:
        """Teszteli a config manager függőség ellenőrzését nem létező fájl esetén."""
        # Arrange
        config = {"config_file_path": "/nonexistent/config.yml"}

        # Act & Assert
        with pytest.raises(ConfigurationError, match="Config file does not exist"):
            CoreComponentFactory._validate_dependencies("config_manager", config)

    @mock.patch("neural_ai.core.config.factory.ConfigManagerFactory")
    @mock.patch("neural_ai.core.logger.factory.LoggerFactory")
    @mock.patch("neural_ai.core.storage.implementations.file_storage.FileStorage")
    def test_create_components_success(self, mock_storage: Any, mock_logger_factory: Any, mock_config_factory: Any) -> None:
        """Teszteli a komponensek sikeres létrehozását."""
        # Arrange
        mock_config = mock.Mock()
        mock_config.get_section.return_value = {"level": "INFO"}
        mock_config_factory.get_manager.return_value = mock_config

        mock_logger = mock.Mock()
        mock_logger_factory.get_logger.return_value = mock_logger

        mock_storage_instance = mock.Mock()
        mock_storage.return_value = mock_storage_instance

        # Act
        components = CoreComponentFactory.create_components(
            config_path="tests/config.yml",
            log_path="app.log",
            storage_path="/tmp/storage"
        )

        # Assert
        assert components is not None
        mock_config_factory.get_manager.assert_called_once_with("tests/config.yml")
        mock_logger_factory.get_logger.assert_called_once()
        mock_storage.assert_called_once_with(base_path="/tmp/storage")

    def test_create_with_container(self) -> None:
        """Teszteli a komponensek létrehozását meglévő konténerből."""
        # Arrange
        container = DIContainer()

        # Act
        components = CoreComponentFactory.create_with_container(container)

        # Assert
        assert components is not None
        assert components._container == container

    @mock.patch("neural_ai.core.config.factory.ConfigManagerFactory")
    @mock.patch("neural_ai.core.logger.factory.LoggerFactory")
    @mock.patch("neural_ai.core.storage.implementations.file_storage.FileStorage")
    def test_create_minimal_success(self, mock_storage: Any, mock_logger_factory: Any, mock_config_factory: Any) -> None:
        """Teszteli a minimális komponensek sikeres létrehozását."""
        # Arrange
        mock_config_factory.get_manager.side_effect = FileNotFoundError()
        mock_logger = mock.Mock()
        mock_logger_factory.get_logger.return_value = mock_logger
        mock_storage_instance = mock.Mock()
        mock_storage.return_value = mock_storage_instance

        # Act
        components = CoreComponentFactory.create_minimal()

        # Assert
        assert components is not None
        mock_logger_factory.get_logger.assert_called_once()
        mock_storage.assert_called_once()

    @mock.patch("neural_ai.core.logger.factory.LoggerFactory")
    def test_create_logger_success(self, mock_logger_factory: Any) -> None:
        """Teszteli a logger sikeres létrehozását."""
        # Arrange
        mock_logger = mock.Mock()
        mock_logger_factory.get_logger.return_value = mock_logger

        # Act
        logger = CoreComponentFactory.create_logger(name="test_logger")

        # Assert
        assert logger == mock_logger
        mock_logger_factory.get_logger.assert_called_once_with(name="test_logger", config={"name": "test_logger"})

    def test_create_logger_missing_name(self) -> None:
        """Teszteli a logger létrehozását hiányzó névvel."""
        # Act & Assert
        with pytest.raises(ConfigurationError, match="Logger name not configured"):
            CoreComponentFactory.create_logger(name="")

    @mock.patch("neural_ai.core.config.factory.ConfigManagerFactory")
    def test_create_config_manager_success(self, mock_config_factory: Any) -> None:
        """Teszteli a config manager sikeres létrehozását."""
        # Arrange
        mock_config = mock.Mock()
        mock_config_factory.get_manager.return_value = mock_config

        # Act
        config_manager = CoreComponentFactory.create_config_manager(
            config_file_path="tests/config.yml"
        )

        # Assert
        assert config_manager == mock_config
        mock_config_factory.get_manager.assert_called_once_with("tests/config.yml")

    def test_create_config_manager_missing_path(self) -> None:
        """Teszteli a config manager létrehozását hiányzó fájlútvonalal."""
        # Act & Assert
        with pytest.raises(ConfigurationError, match="Config file path not configured"):
            CoreComponentFactory.create_config_manager(config_file_path="")

    @mock.patch("neural_ai.core.storage.implementations.file_storage.FileStorage")
    def test_create_storage_success(self, mock_storage: Any) -> None:
        """Teszteli a storage sikeres létrehozását."""
        # Arrange
        mock_storage_instance = mock.Mock()
        mock_storage.return_value = mock_storage_instance

        # Act
        storage = CoreComponentFactory.create_storage(base_directory="/tmp/storage")

        # Assert
        assert storage == mock_storage_instance
        mock_storage.assert_called_once_with(base_path="/tmp/storage")

    def test_create_storage_missing_base_directory(self) -> None:
        """Teszteli a storage létrehozását hiányzó alapkönyvtárral."""
        # Act & Assert
        with pytest.raises(ConfigurationError, match="Storage base_directory not configured"):
            CoreComponentFactory.create_storage(base_directory="")

    def test_lazy_properties(self) -> None:
        """Teszteli a lazy property-k működését."""
        # Arrange
        container = DIContainer()
        factory = CoreComponentFactory(container)

        # Mock-oljuk a config_manager property-t
        mock_config = mock.Mock()
        mock_config.get.return_value = {"test": "value"}
        factory._config_loader = mock.Mock()
        factory._config_loader.return_value = mock_config

        # Act
        # Először hozzáféréskor számolja ki
        result1 = factory._expensive_config
        result2 = factory._expensive_config

        # Assert
        # Csak egyszer hívódik meg a _process_config
        assert result1 == result2
        mock_config.get.assert_called_once()

    def test_get_logger_property(self) -> None:
        """Teszteli a logger property működését."""
        # Arrange
        container = DIContainer()
        factory = CoreComponentFactory(container)

        mock_logger = mock.Mock()
        factory._logger_loader = mock.Mock()
        factory._logger_loader.return_value = mock_logger

        # Act
        result = factory.logger

        # Assert
        assert result == mock_logger
        factory._logger_loader.assert_called_once()

    def test_get_config_manager_property(self) -> None:
        """Teszteli a config_manager property működését."""
        # Arrange
        container = DIContainer()
        factory = CoreComponentFactory(container)

        mock_config = mock.Mock()
        factory._config_loader = mock.Mock()
        factory._config_loader.return_value = mock_config

        # Act
        result = factory.config_manager

        # Assert
        assert result == mock_config
        factory._config_loader.assert_called_once()

    def test_get_storage_property(self) -> None:
        """Teszteli a storage property működését."""
        # Arrange
        container = DIContainer()
        factory = CoreComponentFactory(container)

        mock_storage = mock.Mock()
        factory._storage_loader = mock.Mock()
        factory._storage_loader.return_value = mock_storage

        # Act
        result = factory.storage

        # Assert
        assert result == mock_storage
        factory._storage_loader.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
