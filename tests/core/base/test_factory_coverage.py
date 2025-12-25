"""Additional coverage tests for CoreComponentFactory to reach 100% coverage."""


import pytest

from neural_ai.core.base.exceptions import DependencyError
from neural_ai.core.base.factory import CoreComponentFactory
from neural_ai.core.base.implementations.di_container import DIContainer
from neural_ai.core.logger.implementations.default_logger import DefaultLogger


class TestCoreComponentFactoryCoverage:
    """Additional tests to cover missing lines in CoreComponentFactory."""

    def test_get_logger_with_fallback(self) -> None:
        """Teszteli a logger lekérdezést fallback-kel (Missing line 53-65)."""
        # Arrange
        container = DIContainer()
        factory = CoreComponentFactory(container)

        # Act
        logger = factory._get_logger()

        # Assert
        assert isinstance(logger, DefaultLogger)
        assert logger is not None

    def test_get_config_manager_raises_dependency_error(self) -> None:
        """Teszteli a config manager lekérdezést, ha nincs elérhető (Missing line 69-78)."""
        # Arrange
        container = DIContainer()
        factory = CoreComponentFactory(container)

        # Act & Assert
        with pytest.raises(DependencyError, match="ConfigManager not available"):
            factory._get_config_manager()

    def test_get_storage_raises_dependency_error(self) -> None:
        """Teszteli a storage lekérdezést, ha nincs elérhető (Missing line 82-89)."""
        # Arrange
        container = DIContainer()
        factory = CoreComponentFactory(container)

        # Act & Assert
        with pytest.raises(DependencyError, match="Storage not available"):
            factory._get_storage()

    def test_process_config_returns_config(self) -> None:
        """Teszteli a _process_config metódust (Missing line 119)."""
        # Arrange
        container = DIContainer()
        factory = CoreComponentFactory(container)
        test_config = {"test": "value"}

        # Act
        result = factory._process_config(test_config)

        # Assert
        assert result == test_config

    def test_load_component_cache_returns_empty_dict(self) -> None:
        """Teszteli a _load_component_cache metódust (Missing line 129)."""
        # Arrange
        container = DIContainer()
        factory = CoreComponentFactory(container)

        # Act
        result = factory._load_component_cache()

        # Assert
        assert result == {}

    def test_create_components_without_config(self) -> None:
        """Teszteli a komponensek létrehozását konfig nélkül (Missing lines)."""
        # Act
        components = CoreComponentFactory.create_components()

        # Assert
        assert components is not None
        assert components._container is not None

    def test_create_components_with_config_only(self) -> None:
        """Teszteli a komponensek létrehozását csak konfiggal."""
        # Act
        components = CoreComponentFactory.create_components(
            config_path="tests/config.yml"
        )

        # Assert
        assert components is not None

    def test_create_minimal_with_existing_config(self) -> None:
        """Teszteli a minimális komponensek létrehozását létező configgel."""
        # Ez a teszt lefedi a 307-308 sorokat, ahol a config létezik
        # Act
        components = CoreComponentFactory.create_minimal()

        # Assert
        assert components is not None

    def test_create_logger_with_config_dict(self) -> None:
        """Teszteli a logger létrehozását konfigurációs dictionary-vel."""
        # Arrange
        config = {"name": "test_logger", "level": "DEBUG"}

        # Act
        logger = CoreComponentFactory.create_logger(name="test_logger", config=config)

        # Assert
        assert logger is not None

    def test_create_config_manager_with_config_dict(self) -> None:
        """Teszteli a config manager létrehozását konfigurációs dictionary-vel."""
        # Act
        config_manager = CoreComponentFactory.create_config_manager(
            config_file_path="tests/config.yml",
            config={"test": "value"}
        )

        # Assert
        assert config_manager is not None

    def test_create_storage_with_config_dict(self) -> None:
        """Teszteli a storage létrehozását konfigurációs dictionary-vel."""
        # Act
        storage = CoreComponentFactory.create_storage(
            base_directory="/tmp/test",
            config={"test": "value"}
        )

        # Assert
        assert storage is not None
