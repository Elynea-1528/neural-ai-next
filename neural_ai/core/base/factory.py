"""Core komponensek factory implementáció."""

import time
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, Optional, Union

from neural_ai.core.base.container import DIContainer
from neural_ai.core.base.exceptions import (
    ConfigurationError,
    DependencyError,
)
from neural_ai.core.base.lazy_loading import LazyLoader, lazy_property
from neural_ai.core.base.singleton import SingletonMeta
from neural_ai.core.config.exceptions import ConfigLoadError
from neural_ai.core.config.implementations import ConfigManagerFactory
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.logger.implementations import LoggerFactory
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
from neural_ai.core.storage.implementations.file_storage import FileStorage
from neural_ai.core.storage.interfaces.storage_interface import StorageInterface

if TYPE_CHECKING:
    from neural_ai.core.base.core_components import CoreComponents


class CoreComponentFactory(metaclass=SingletonMeta):
    """Factory for creating core components with lazy loading."""

    def __init__(self, container: DIContainer):
        """Initialize the factory with lazy-loaded dependencies."""
        self._container = container
        self._logger_loader = LazyLoader(self._get_logger)
        self._config_loader = LazyLoader(self._get_config_manager)
        self._storage_loader = LazyLoader(self._get_storage)

    def _get_logger(self) -> LoggerInterface:
        """Lazy load the logger."""
        logger = self._container.resolve(LoggerInterface)
        if logger is not None:
            assert isinstance(logger, LoggerInterface), (
                "Logger must implement LoggerInterface"
            )
            return logger
        
        # Fallback to default logger
        from neural_ai.core.logger.implementations.default_logger import (
            DefaultLogger,
        )

        return DefaultLogger(name="CoreComponentFactory")

    def _get_config_manager(self) -> ConfigManagerInterface:
        """Lazy load the config manager."""
        config_manager = self._container.resolve(ConfigManagerInterface)
        if config_manager is not None:
            assert isinstance(config_manager, ConfigManagerInterface), (
                "ConfigManager must implement ConfigManagerInterface"
            )
            return config_manager
        
        raise DependencyError("ConfigManager not available")

    def _get_storage(self) -> StorageInterface:
        """Lazy load the storage."""
        storage = self._container.resolve(StorageInterface)
        if storage is not None:
            assert isinstance(storage, StorageInterface), (
                "Storage must implement StorageInterface"
            )
            return storage
        
        raise DependencyError("Storage not available")

    @property
    def logger(self) -> LoggerInterface:
        """Get the logger instance (lazy-loaded)."""
        return self._logger_loader()

    @property
    def config_manager(self) -> ConfigManagerInterface:
        """Get the config manager instance (lazy-loaded)."""
        return self._config_loader()

    @property
    def storage(self) -> StorageInterface:
        """Get the storage instance (lazy-loaded)."""
        return self._storage_loader()

    @lazy_property
    def _expensive_config(self) -> Dict[str, Any]:
        """Lazy load expensive configuration."""
        # This will only be computed once when first accessed
        config = self.config_manager.get()
        # Perform expensive processing
        time.sleep(1)  # Simulate expensive operation
        return self._process_config(config)

    @lazy_property
    def _component_cache(self) -> Dict[str, Any]:
        """Lazy load component cache."""
        # This will only be computed once when first accessed
        return self._load_component_cache()

    def _process_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Process configuration (simulated expensive operation)."""
        # Add processing logic here
        return config

    def _load_component_cache(self) -> Dict[str, Any]:
        """Load component cache (simulated expensive operation)."""
        # Add cache loading logic here
        return {}

    def reset_lazy_loaders(self) -> None:
        """Reset all lazy loaders (useful for testing)."""
        self._logger_loader.reset()
        self._config_loader.reset()
        self._storage_loader.reset()

        # Clear lazy properties
        for attr_name in dir(self):
            if attr_name.startswith("_lazy_"):
                delattr(self, attr_name)

    @staticmethod
    def _validate_dependencies(
        component_type: str, config: Optional[Dict[str, Any]] = None
    ) -> None:
        """Validate that all required dependencies are available.

        Args:
            component_type: The type of component being created
            config: Configuration dictionary

        Raises:
            ConfigurationError: If configuration is invalid or missing
            DependencyError: If required dependencies are not available
        """
        config = config or {}

        # Create a temporary container instance to check for dependencies
        temp_container = DIContainer()

        # Check logger dependency (required for all components)
        logger = temp_container.resolve(LoggerInterface)
        if logger is None:
            raise DependencyError(
                f"Logger not initialized. Required for {component_type}. "
                "Call container.register_instance(LoggerInterface, logger_instance) first."
            )

        # Check config manager dependency (required for all components)
        config_manager = temp_container.resolve(ConfigManagerInterface)
        if config_manager is None:
            raise DependencyError(
                f"ConfigManager not initialized. Required for {component_type}. "
                "Call container.register_instance(ConfigManagerInterface, config_manager_instance) first."
            )

        # Type-specific validations
        if component_type == "storage":
            # Check if storage directory is configured
            if not config.get("base_directory"):
                raise ConfigurationError(
                    "Storage base_directory not configured. "
                    "Provide 'base_directory' in config dictionary."
                )

            # Check if base_directory is a valid path
            base_dir = Path(config["base_directory"])
            if not base_dir.parent.exists():
                raise ConfigurationError(
                    f"Storage base_directory parent does not exist: {base_dir.parent}"
                )

        elif component_type == "logger":
            # Check if logger name is provided
            if not config.get("name"):
                raise ConfigurationError(
                    "Logger name not configured. Provide 'name' in config dictionary."
                )

        elif component_type == "config_manager":
            # Check if config file path is provided
            if not config.get("config_file_path"):
                raise ConfigurationError(
                    "Config file path not configured. Provide 'config_file_path' in config dictionary."
                )

            # Check if config file exists
            config_path = Path(config["config_file_path"])
            if not config_path.exists():
                raise ConfigurationError(f"Config file does not exist: {config_path}")

    @staticmethod
    def create_components(
        config_path: Optional[Union[str, Path]] = None,
        log_path: Optional[Union[str, Path]] = None,
        storage_path: Optional[Union[str, Path]] = None,
    ) -> "CoreComponents":
        """Core komponensek létrehozása és inicializálása."""
        from neural_ai.core.base.core_components import CoreComponents
        container = DIContainer()

        # 1. Config komponens létrehozása
        config: Optional[ConfigManagerInterface] = None
        if config_path:
            config = ConfigManagerFactory.get_manager(str(config_path))
            container.register_instance(ConfigManagerInterface, config)

        # 2. Logger komponens létrehozása
        logger: Optional[LoggerInterface] = None
        if config or log_path:
            log_config: Dict[str, Any] = {}
            if log_path:
                log_config["log_file"] = str(log_path)
            if config:
                logger_section = config.get_section("logger")
                if logger_section:
                    log_config.update(logger_section)

            logger = LoggerFactory.get_logger(name="core", config=log_config)
            container.register_instance(LoggerInterface, logger)

        # 3. Storage komponens létrehozása a konfiggal és loggerrel
        storage: Optional[StorageInterface] = None
        if storage_path:
            from neural_ai.core.storage.implementations.file_storage import FileStorage

            storage = FileStorage(base_path=storage_path)
            container.register_instance(StorageInterface, storage)

        # 4. Komponensek összekötése
        components = CoreComponents(container=container)

        # 5. Komponensek validálása
        if not components.validate():
            if logger:
                logger.warning("Nem minden core komponens került inicializálásra")

        return components

    @staticmethod
    def create_with_container(container: DIContainer) -> "CoreComponents":
        """Core komponensek létrehozása meglévő konténerből."""
        from neural_ai.core.base.core_components import CoreComponents
        return CoreComponents(container=container)

    @staticmethod
    def create_minimal() -> "CoreComponents":
        """Minimális core komponens készlet létrehozása."""
        from neural_ai.core.base.core_components import CoreComponents
        config = None
        log_config: Dict[str, Any] = {}

        try:
            config = ConfigManagerFactory.get_manager("config.yml")
            if config:
                logger_section = config.get_section("logger")
                if logger_section:
                    log_config = logger_section
        except (FileNotFoundError, ConfigLoadError):
            # Ha a config.yml fájl nem létezik, alapértelmezett konfigurációt használunk
            config = None
            log_config = {
                "level": "INFO",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            }

        logger = LoggerFactory.get_logger(name="core", config=log_config)
        storage = FileStorage()

        # Create a temporary container to validate dependencies
        container = DIContainer()
        if config:
            container.register_instance(ConfigManagerInterface, config)
        if logger:
            container.register_instance(LoggerInterface, logger)
        if storage:
            container.register_instance(StorageInterface, storage)

        return CoreComponents(container=container)

    @staticmethod
    def create_logger(
        name: str, config: Optional[Dict[str, Any]] = None
    ) -> LoggerInterface:
        """Create a logger instance.

        Args:
            name: The name of the logger
            config: Configuration dictionary

        Returns:
            LoggerInterface: The created logger instance

        Raises:
            ConfigurationError: If configuration is invalid
            DependencyError: If required dependencies are missing
        """
        config = config or {}
        config["name"] = name

        # Validate dependencies
        CoreComponentFactory._validate_dependencies("logger", config)

        # Create logger using LoggerFactory
        return LoggerFactory.get_logger(name=name, config=config)

    @staticmethod
    def create_config_manager(
        config_file_path: str, config: Optional[Dict[str, Any]] = None
    ) -> ConfigManagerInterface:
        """Create a config manager instance.

        Args:
            config_file_path: Path to the configuration file
            config: Configuration dictionary

        Returns:
            ConfigManagerInterface: The created config manager instance

        Raises:
            ConfigurationError: If configuration is invalid
            DependencyError: If required dependencies are missing
        """
        config = config or {}
        config["config_file_path"] = config_file_path

        # Validate dependencies
        CoreComponentFactory._validate_dependencies("config_manager", config)

        # Create config manager using ConfigManagerFactory
        return ConfigManagerFactory.get_manager(config_file_path)

    @staticmethod
    def create_storage(
        base_directory: str, config: Optional[Dict[str, Any]] = None
    ) -> StorageInterface:
        """Create a storage instance.

        Args:
            base_directory: The base directory for storage
            config: Configuration dictionary

        Returns:
            StorageInterface: The created storage instance

        Raises:
            ConfigurationError: If configuration is invalid
            DependencyError: If required dependencies are missing
        """
        config = config or {}
        config["base_directory"] = base_directory

        # Validate dependencies
        CoreComponentFactory._validate_dependencies("storage", config)

        # Create storage instance
        return FileStorage(base_path=base_directory)
