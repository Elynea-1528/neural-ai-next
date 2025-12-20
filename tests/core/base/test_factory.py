"""Core komponensek factory tesztek."""

from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from neural_ai.core.base.core_components import CoreComponents
from neural_ai.core.base.factory import CoreComponentFactory
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
from neural_ai.core.storage.interfaces.storage_interface import StorageInterface


@pytest.fixture
def mock_config() -> Mock:
    """Mock config komponens."""
    config = Mock(spec=ConfigManagerInterface)
    config.get_section.return_value = {"level": "INFO"}
    return config


@pytest.fixture
def mock_logger() -> Mock:
    """Mock logger komponens."""
    return Mock(spec=LoggerInterface)


@pytest.fixture
def mock_storage() -> Mock:
    """Mock storage komponens."""
    return Mock(spec=StorageInterface)


def test_create_components_with_all_params(tmp_path: Path) -> None:
    """Teszteli a komponensek létrehozását minden paraméterrel."""
    config_path = tmp_path / "config.yml"
    log_path = tmp_path / "app.log"
    storage_path = tmp_path / "data"

    with (
        patch("neural_ai.core.base.factory.ConfigManagerFactory") as config_factory,
        patch("neural_ai.core.base.factory.LoggerFactory") as logger_factory,
        patch("neural_ai.core.base.factory.FileStorage") as storage_class,
    ):
        # Mock komponensek beállítása
        mock_config = Mock(spec=ConfigManagerInterface)
        mock_config.get_section.return_value = {"level": "INFO"}
        config_factory.get_manager.return_value = mock_config

        mock_logger = Mock(spec=LoggerInterface)
        logger_factory.get_logger.return_value = mock_logger

        mock_storage = Mock(spec=StorageInterface)
        storage_class.return_value = mock_storage

        # Komponensek létrehozása
        components = CoreComponentFactory.create_components(
            config_path=config_path,
            log_path=log_path,
            storage_path=storage_path,
        )

        # Ellenőrzések
        assert isinstance(components, CoreComponents)
        assert components.config == mock_config
        assert components.logger == mock_logger
        assert components.storage == mock_storage

        # Factory hívások ellenőrzése
        config_factory.get_manager.assert_called_once_with(str(config_path))
        logger_factory.get_logger.assert_called_once()
        storage_class.assert_called_once_with(base_path=storage_path)


def test_create_components_minimal() -> None:
    """Teszteli a komponensek létrehozását minimális paraméterekkel."""
    components = CoreComponentFactory.create_components()

    assert isinstance(components, CoreComponents)
    assert components.config is None
    assert components.logger is None
    assert components.storage is None


def test_create_with_container(mock_config: Mock, mock_logger: Mock, mock_storage: Mock) -> None:
    """Teszteli a komponensek létrehozását konténerből."""
    container = Mock()
    container.resolve.side_effect = lambda t: {
        ConfigManagerInterface: mock_config,
        LoggerInterface: mock_logger,
        StorageInterface: mock_storage,
    }[t]

    components = CoreComponentFactory.create_with_container(container)

    assert isinstance(components, CoreComponents)
    assert components.config == mock_config
    assert components.logger == mock_logger
    assert components.storage == mock_storage


def test_create_minimal_with_mocks() -> None:
    """Teszteli az alap komponensek létrehozását mock-okkal."""
    with (
        patch("neural_ai.core.base.factory.ConfigManagerFactory") as config_factory,
        patch("neural_ai.core.base.factory.LoggerFactory") as logger_factory,
        patch("neural_ai.core.base.factory.FileStorage") as storage_class,
    ):
        # Mock komponensek beállítása
        mock_config = Mock(spec=ConfigManagerInterface)
        mock_config.get_section.return_value = {"level": "INFO"}
        config_factory.get_manager.return_value = mock_config

        mock_logger = Mock(spec=LoggerInterface)
        logger_factory.get_logger.return_value = mock_logger

        mock_storage = Mock(spec=StorageInterface)
        storage_class.return_value = mock_storage

        # Komponensek létrehozása
        components = CoreComponentFactory.create_minimal()

        # Ellenőrzések
        assert isinstance(components, CoreComponents)
        assert components.config == mock_config
        assert components.logger == mock_logger
        assert components.storage == mock_storage

        # Factory hívások ellenőrzése
        config_factory.get_manager.assert_called_once_with("config.yml")
        logger_factory.get_logger.assert_called_once_with(name="core", config={"level": "INFO"})
        storage_class.assert_called_once_with()


def test_create_components_with_warning_log() -> None:
    """Teszteli a warning logolást hiányzó komponensek esetén."""
    with patch("neural_ai.core.base.factory.LoggerFactory") as logger_factory:
        # Csak logger komponens létrehozása
        mock_logger = Mock(spec=LoggerInterface)
        logger_factory.get_logger.return_value = mock_logger

        # Komponensek létrehozása csak loggerrel
        components = CoreComponentFactory.create_components(log_path="test.log")
        assert not components.validate()

        # Ellenőrizzük, hogy a warning log megtörtént
        mock_logger.warning.assert_called_once_with(
            "Nem minden core komponens került inicializálásra"
        )


def test_create_logger() -> None:
    """Teszteli a logger létrehozását."""
    with (
        patch("neural_ai.core.base.factory.LoggerFactory") as logger_factory,
        patch("neural_ai.core.base.factory.DIContainer") as container_class,
    ):
        mock_logger = Mock(spec=LoggerInterface)
        logger_factory.get_logger.return_value = mock_logger

        # Mock container for validation
        mock_container = Mock()
        mock_container.resolve.return_value = mock_logger
        container_class.return_value = mock_container

        logger = CoreComponentFactory.create_logger("test_logger", {"level": "DEBUG"})

        assert logger == mock_logger
        logger_factory.get_logger.assert_called_once_with(
            name="test_logger", config={"name": "test_logger", "level": "DEBUG"}
        )


def test_create_config_manager(tmp_path: Path) -> None:
    """Teszteli a config manager létrehozását."""
    config_file = tmp_path / "test_config.yaml"
    config_file.write_text("test: config")

    with (
        patch("neural_ai.core.base.factory.ConfigManagerFactory") as config_factory,
        patch("neural_ai.core.base.factory.DIContainer") as container_class,
    ):
        mock_config = Mock(spec=ConfigManagerInterface)
        config_factory.get_manager.return_value = mock_config

        # Mock container for validation
        mock_container = Mock()
        mock_container.resolve.return_value = Mock(spec=LoggerInterface)
        container_class.return_value = mock_container

        config = CoreComponentFactory.create_config_manager(str(config_file), {"extra": "value"})

        assert config == mock_config
        config_factory.get_manager.assert_called_once_with(str(config_file))


def test_create_storage() -> None:
    """Teszteli a storage létrehozását."""
    with (
        patch("neural_ai.core.base.factory.FileStorage") as storage_class,
        patch("neural_ai.core.base.factory.DIContainer") as container_class,
    ):
        mock_storage = Mock(spec=StorageInterface)
        storage_class.return_value = mock_storage

        # Mock container for validation
        mock_container = Mock()
        mock_container.resolve.return_value = Mock(spec=LoggerInterface)
        container_class.return_value = mock_container

        storage = CoreComponentFactory.create_storage("/tmp/test", {"option": "value"})

        assert storage == mock_storage
        storage_class.assert_called_once_with(base_path="/tmp/test")


def test_factory_instance_properties() -> None:
    """Teszteli a factory példány property-jeit."""
    container = Mock()
    mock_logger = Mock(spec=LoggerInterface)
    mock_config = Mock(spec=ConfigManagerInterface)
    mock_storage = Mock(spec=StorageInterface)

    container.resolve.side_effect = lambda t: {
        LoggerInterface: mock_logger,
        ConfigManagerInterface: mock_config,
        StorageInterface: mock_storage,
    }.get(t)

    factory = CoreComponentFactory(container)

    # Test properties
    logger = factory.logger
    config_manager = factory.config_manager
    storage = factory.storage

    assert logger == mock_logger
    assert config_manager == mock_config
    assert storage == mock_storage

    # Test reset
    factory.reset_lazy_loaders()
    # Should work without errors
