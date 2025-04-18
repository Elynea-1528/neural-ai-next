"""Core komponensek tesztek."""

from unittest.mock import Mock

import pytest

from neural_ai.core.base.core_components import CoreComponents
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
from neural_ai.core.storage.interfaces.storage_interface import StorageInterface


@pytest.fixture
def components() -> CoreComponents:
    """Core komponensek fixture."""
    return CoreComponents()


@pytest.fixture
def mock_config() -> Mock:
    """Mock config komponens."""
    return Mock(spec=ConfigManagerInterface)


@pytest.fixture
def mock_logger() -> Mock:
    """Mock logger komponens."""
    return Mock(spec=LoggerInterface)


@pytest.fixture
def mock_storage() -> Mock:
    """Mock storage komponens."""
    return Mock(spec=StorageInterface)


def test_empty_components(components: CoreComponents) -> None:
    """Teszteli az üres komponens készletet."""
    assert not components.has_config()
    assert not components.has_logger()
    assert not components.has_storage()
    assert not components.validate()


def test_has_config(components: CoreComponents, mock_config: Mock) -> None:
    """Teszteli a config komponens meglétének ellenőrzését."""
    assert not components.has_config()
    components.config = mock_config
    assert components.has_config()


def test_has_logger(components: CoreComponents, mock_logger: Mock) -> None:
    """Teszteli a logger komponens meglétének ellenőrzését."""
    assert not components.has_logger()
    components.logger = mock_logger
    assert components.has_logger()


def test_has_storage(components: CoreComponents, mock_storage: Mock) -> None:
    """Teszteli a storage komponens meglétének ellenőrzését."""
    assert not components.has_storage()
    components.storage = mock_storage
    assert components.has_storage()


def test_validate_all_components(
    components: CoreComponents,
    mock_config: Mock,
    mock_logger: Mock,
    mock_storage: Mock,
) -> None:
    """Teszteli az összes komponens validálását."""
    assert not components.validate()

    components.config = mock_config
    assert not components.validate()

    components.logger = mock_logger
    assert not components.validate()

    components.storage = mock_storage
    assert components.validate()


def test_validate_missing_components(
    components: CoreComponents,
    mock_config: Mock,
    mock_logger: Mock,
    mock_storage: Mock,
) -> None:
    """Teszteli a komponensek validálását hiányzó komponensekkel."""
    # Csak config
    components.config = mock_config
    assert not components.validate()

    # Csak logger
    components = CoreComponents(logger=mock_logger)
    assert not components.validate()

    # Csak storage
    components = CoreComponents(storage=mock_storage)
    assert not components.validate()

    # Config és logger
    components = CoreComponents(config=mock_config, logger=mock_logger)
    assert not components.validate()

    # Config és storage
    components = CoreComponents(config=mock_config, storage=mock_storage)
    assert not components.validate()

    # Logger és storage
    components = CoreComponents(logger=mock_logger, storage=mock_storage)
    assert not components.validate()
