"""Core komponensek factory implementáció.

Ez a modul biztosítja a core komponensek (config, logger, storage) létrehozását
és kezelését dependency injection pattern használatával. A factory támogatja
a lazy loadinget, bootstrap inicializálást és NullObject pattern-t fallback-ként.
"""

import time
from pathlib import Path
from typing import TYPE_CHECKING, Any, TypedDict, cast

from neural_ai.core.base.exceptions import (
    ConfigurationError,
    DependencyError,
)
from neural_ai.core.base.implementations.di_container import DIContainer
from neural_ai.core.base.implementations.lazy_loader import LazyLoader, lazy_property
from neural_ai.core.base.implementations.singleton import SingletonMeta
from neural_ai.core.logger.factory import LoggerFactory  # Added for DI compliance
from neural_ai.core.utils.decorators import trace

DEFAULT_CONFIG_FILE = "config.yml"


class BaseConfig(TypedDict, total=False):
    """Alap konfigurációs schema."""


class LoggerConfig(BaseConfig):
    """Logger komponens konfigurációja."""

    name: str
    level: str
    format: str
    log_file: str


class ConfigManagerConfig(BaseConfig):
    """Config manager komponens konfigurációja."""

    config_file_path: str


class StorageConfig(BaseConfig):
    """Storage komponens konfigurációja."""

    base_directory: str


if TYPE_CHECKING:
    from neural_ai.core.base.implementations.component_bundle import CoreComponents
    from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
    from neural_ai.data.storage.interfaces.storage_interface import StorageInterface


class CoreComponentFactory(metaclass=SingletonMeta):
    """Core komponensek létrehozásáért felelős factory lazy loadinggel.

    Ez az osztály biztosítja a core komponensek (config, logger, storage) egységes
    létrehozását és kezelését. Singleton minta használatával biztosítja, hogy csak
    egy példány létezik, és lazy loading technikával optimalizálja a teljesítményt.

    A factory támogatja a komponensek validációját, függőségi injektálást és
    automatikus inicializálást különböző konfigurációs forgatókönyvekben.

    Attributes:
        _container: A dependency injection konténer
        _logger_loader: Lazy loader a logger komponenshez
        _config_loader: Lazy loader a config manager komponenshez
        _storage_loader: Lazy loader a storage komponenshez
    """

    def __init__(self, container: DIContainer):
        """Inicializálja a factory-t lazy-loaded függőségekkel."""
        self._container = container
        self._logger_loader = LazyLoader(self._get_logger)
        self._config_loader = LazyLoader(self._get_config_manager)
        self._storage_loader = LazyLoader(self._get_storage)

    def _get_logger(self) -> "LoggerInterface":
        """Lazy loadinggel tölti be a logger komponenst."""
        from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface

        logger = self._container.resolve(LoggerInterface)
        if logger is not None:
            assert isinstance(logger, LoggerInterface), "Logger must implement LoggerInterface"
            return cast(LoggerInterface, logger)

        # Fallback to default logger (NullObject pattern)
        return LoggerFactory.get_logger(__name__)

    def _get_config_manager(self) -> "ConfigManagerInterface":
        """Lazy loadinggel tölti be a config manager komponenst."""
        from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface

        config_manager = self._container.resolve(ConfigManagerInterface)
        if config_manager is not None:
            assert isinstance(config_manager, ConfigManagerInterface), (
                "ConfigManager must implement ConfigManagerInterface"
            )
            return cast(ConfigManagerInterface, config_manager)

        raise DependencyError("ConfigManager not available")

    def _get_storage(self) -> "StorageInterface":
        """Lazy loadinggel tölti be a storage komponenst."""
        from neural_ai.data.storage.interfaces.storage_interface import StorageInterface

        storage = self._container.resolve(StorageInterface)
        if storage is not None:
            assert isinstance(storage, StorageInterface), "Storage must implement StorageInterface"
            return cast(StorageInterface, storage)

        raise DependencyError("Storage not available")

    @property
    def logger(self) -> "LoggerInterface":
        """Visszaadja a logger példányt (lazy-loaded)."""
        return self._logger_loader()

    @property
    def config_manager(self) -> "ConfigManagerInterface":
        """Visszaadja a config manager példányt (lazy-loaded)."""
        return self._config_loader()

    @property
    def storage(self) -> "StorageInterface":
        """Visszaadja a storage példányt (lazy-loaded)."""
        return self._storage_loader()

    @lazy_property
    def _expensive_config(self) -> dict[str, Any]:
        """Lazy loadinggel tölti be a drága konfigurációt."""
        # This will only be computed once when first accessed
        config = self.config_manager.get()
        # Perform expensive processing
        time.sleep(1)  # Simulate expensive operation
        return self._process_config(config)

    @lazy_property
    def _component_cache(self) -> dict[str, Any]:
        """Lazy loadinggel tölti be a komponens gyorsítótárát."""
        # This will only be computed once when first accessed
        return self._load_component_cache()

    def _process_config(self, config: dict[str, Any]) -> dict[str, Any]:
        """Feldolgozza a konfigurációt (szimulált drága művelet)."""
        # Add processing logic here
        return config

    def _load_component_cache(self) -> dict[str, Any]:
        """Betölti a komponens gyorsítótárát (szimulált drága művelet)."""
        # Add cache loading logic here
        return {}

    def reset_lazy_loaders(self) -> None:
        """Visszaállítja az összes lazy loadert.

        Ez a metódus visszaállítja az összes lazy loader állapotát, amely
        hasznos lehet tesztelés során vagy újrainicializáláskor.
        A lazy property-ket is törli.
        """
        self._logger_loader.reset()
        self._config_loader.reset()
        self._storage_loader.reset()

        # Clear lazy properties
        for attr_name in dir(self):
            if attr_name.startswith("_lazy_"):
                delattr(self, attr_name)

    @staticmethod
    def _validate_dependencies(component_type: str, config: dict[str, Any] | None = None) -> None:
        """Ellenőrzi, hogy minden szükséges függőség elérhető-e.

        Args:
            component_type: A létrehozandó komponens típusa
            config: Konfigurációs dictionary

        Raises:
            ConfigurationError: Ha a konfiguráció érvénytelen vagy hiányzik
            DependencyError: Ha szükséges függőségek nem érhetők el
        """
        config = config or {}

        # Megjegyzés: A függőség ellenőrzés mostantól csak a konfigurációs
        # paramétereket ellenőrzi, nem a DI konténert.
        # A DI konténer ellenőrzése a create_components metódusokra vonatkozik.

        # Type-specific validations
        if component_type == "storage":
            # Check if storage directory is configured
            storage_config = cast(StorageConfig, config)
            if not storage_config.get("base_directory"):
                raise ConfigurationError(
                    "Storage base_directory not configured. "
                    "Provide 'base_directory' in config dictionary."
                )

            # Check if base_directory is a valid path
            base_dir = Path(storage_config["base_directory"])
            if not base_dir.parent.exists():
                raise ConfigurationError(
                    f"Storage base_directory parent does not exist: {base_dir.parent}"
                )

        elif component_type == "logger":
            # Check if logger name is provided
            logger_config = cast(LoggerConfig, config)
            if not logger_config.get("name"):
                raise ConfigurationError(
                    "Logger name not configured. Provide 'name' in config dictionary."
                )

        elif component_type == "config_manager":
            # Check if config file path is provided
            config_manager_config = cast(ConfigManagerConfig, config)
            if not config_manager_config.get("config_file_path"):
                raise ConfigurationError(
                    "Config file path not configured. Provide 'config_file_path' in config dict."
                )

            # Check if config file exists
            config_path = Path(config_manager_config["config_file_path"])
            if not config_path.exists():
                raise ConfigurationError(f"Config file does not exist: {config_path}")

    @staticmethod
    @trace
    def create_components(
        config_path: str | Path | None = None,
        log_path: str | Path | None = None,
        storage_path: str | Path | None = None,
    ) -> "CoreComponents":
        """Core komponensek létrehozása és inicializálása.

        Létrehozza és inicializálja az összes core komponenst (config, logger, storage)
        a megadott elérési utak alapján. A komponensek lazy loadinggel kerülnek betöltésre.

        Args:
            config_path: A konfigurációs fájl elérési útja (opcionális)
            log_path: A log fájl elérési útja (opcionális)
            storage_path: A tároló alapkönyvtára (opcionális)

        Returns:
            CoreComponents: Az inicializált core komponensek gyűjteménye

        Raises:
            ConfigurationError: Ha a konfiguráció érvénytelen
            DependencyError: Ha szükséges függőségek hiányoznak
        """
        from neural_ai.core.base.implementations.component_bundle import CoreComponents
        from neural_ai.core.config.factory import ConfigManagerFactory
        from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
        from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
        from neural_ai.data.storage.interfaces.storage_interface import StorageInterface

        container = DIContainer()

        # 1. Config komponens létrehozása
        config: ConfigManagerInterface | None = None
        if config_path:
            config = ConfigManagerFactory.get_manager(str(config_path))
            container.register_instance(ConfigManagerInterface, config)

        # 2. Logger komponens létrehozása
        logger: LoggerInterface | None = None
        if config or log_path:
            log_config: dict[str, Any] = {}
            if log_path:
                log_config["log_file"] = str(log_path)
            if config:
                logger_config = cast(LoggerConfig, config.get("logger") or {})
                if logger_config:
                    log_config.update(logger_config)

            logger = LoggerFactory.get_logger(__name__, config=log_config)
            container.register_instance(LoggerInterface, logger)

        # 3. Storage komponens létrehozása a konfiggal és loggerrel
        storage: StorageInterface | None = None
        if storage_path and logger and config:
            storage = CoreComponentFactory.create_storage(str(storage_path), logger, config)
            container.register_instance(StorageInterface, storage)

        # 4. Komponensek összekötése
        components = CoreComponents(container=container)

        # 5. Komponensek validálása
        if not components.validate():
            if logger:
                logger.warning(
                    "Nem minden core komponens került inicializálásra",
                    extra={"component": "CoreComponentFactory"},
                )

        return components

    @staticmethod
    @trace
    def create_with_container(container: DIContainer) -> "CoreComponents":
        """Core komponensek létrehozása meglévő konténerből.

        Args:
            container: A DI konténer, amely tartalmazza a komponenseket

        Returns:
            CoreComponents: Az inicializált core komponensek
        """
        from neural_ai.core.base.implementations.component_bundle import CoreComponents

        return CoreComponents(container=container)

    @staticmethod
    @trace
    def create_minimal() -> "CoreComponents":
        """Minimális core komponens készlet létrehozása.

        Létrehoz egy alapvető komponens készletet alapértelmezett beállításokkal.
        Megpróbálja betölteni a config.yml fájlt, ha létezik, különben alapértelmezett
        konfigurációt használ.

        Returns:
            CoreComponents: Az inicializált minimális komponensek
        """
        from neural_ai.core.base.implementations.component_bundle import CoreComponents
        from neural_ai.core.config.exceptions import ConfigLoadError
        from neural_ai.core.config.factory import ConfigManagerFactory
        from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
        from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
        from neural_ai.data.storage.implementations.file_storage import FileStorage
        from neural_ai.data.storage.interfaces.storage_interface import StorageInterface

        config = None
        log_config: dict[str, Any] = {}

        try:
            config = ConfigManagerFactory.get_manager(DEFAULT_CONFIG_FILE)
            if config:
                logger_config = cast(LoggerConfig, config.get("logger") or {})
                if logger_config:
                    log_config = dict(logger_config)
        except (FileNotFoundError, ConfigLoadError):
            # Ha a config.yml fájl nem létezik, alapértelmezett konfigurációt használunk
            config = None
            log_config = {
                "level": "INFO",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            }

        logger = LoggerFactory.get_logger(__name__, config=log_config)
        if config:
            storage = CoreComponentFactory.create_storage(None, logger, config)
        else:
            storage = FileStorage(logger=logger)

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
    def create_logger(name: str, config: dict[str, Any] | None = None) -> "LoggerInterface":
        """Létrehoz egy logger példányt.

        Args:
            name: A logger neve
            config: Konfigurációs dictionary (opcionális)

        Returns:
            LoggerInterface: A létrehozott logger példány

        Raises:
            ConfigurationError: Ha a konfiguráció érvénytelen
            DependencyError: Ha szükséges függőségek hiányoznak
        """
        config = config or {}
        config["name"] = name

        # Validate dependencies
        CoreComponentFactory._validate_dependencies("logger", config)

        # Create logger using LoggerFactory

        return LoggerFactory.get_logger(name=name, config=config)

    @staticmethod
    def create_config_manager(
        config_file_path: str, config: dict[str, Any] | None = None
    ) -> "ConfigManagerInterface":
        """Létrehoz egy config manager példányt.

        Args:
            config_file_path: A konfigurációs fájl elérési útja
            config: Konfigurációs dictionary

        Returns:
            ConfigManagerInterface: A létrehozott config manager példány

        Raises:
            ConfigurationError: Ha a konfiguráció érvénytelen
            DependencyError: Ha szükséges függőségek hiányoznak
        """
        config = config or {}
        config["config_file_path"] = config_file_path

        # Validate dependencies
        CoreComponentFactory._validate_dependencies("config_manager", config)

        # Create config manager using ConfigManagerFactory
        from neural_ai.core.config.factory import ConfigManagerFactory

        return ConfigManagerFactory.get_manager(config_file_path)

    @staticmethod
    def create_storage(
        base_directory: str | None, logger: "LoggerInterface", config_manager: "ConfigManagerInterface"
    ) -> "StorageInterface":
        """Létrehoz egy storage példányt.

        Args:
            base_directory: A tároló alapkönyvtára
            logger: Logger interfész példány
            config_manager: Config manager interfész példány

        Returns:
            StorageInterface: A létrehozott storage példány

        Raises:
            ConfigurationError: Ha a konfiguráció érvénytelen
            DependencyError: Ha szükséges függőségek hiányoznak
        """
        config: dict[str, Any] = {}
        if base_directory:
            config["base_directory"] = base_directory
        storage_config = cast(StorageConfig, config_manager.get("storage") or {})
        config.update(storage_config)

        # Validate dependencies
        CoreComponentFactory._validate_dependencies("storage", config)

        # Create storage instance
        from neural_ai.core.events.factory import EventBusFactory
        from neural_ai.data.storage.implementations.file_storage import FileStorage

        event_bus = EventBusFactory.get_event_bus(logger=logger)
        return FileStorage(
            logger=logger, config=config_manager, event_bus=event_bus, base_path=base_directory
        )
