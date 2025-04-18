"""Core komponensek factory implementáció."""

from pathlib import Path
from typing import Any, Dict, Optional, Union

from neural_ai.core.base.container import DIContainer
from neural_ai.core.base.core_components import CoreComponents
from neural_ai.core.config.implementations import ConfigManagerFactory
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.logger.implementations import LoggerFactory
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
from neural_ai.core.storage.implementations.file_storage import FileStorage
from neural_ai.core.storage.interfaces.storage_interface import StorageInterface


class CoreComponentFactory:
    """Factory osztály a core komponensek létrehozásához és konfigurálásához."""

    @staticmethod
    def create_components(
        config_path: Optional[Union[str, Path]] = None,
        log_path: Optional[Union[str, Path]] = None,
        storage_path: Optional[Union[str, Path]] = None,
    ) -> CoreComponents:
        """Core komponensek létrehozása és inicializálása."""
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
                if isinstance(logger_section, dict):
                    log_config.update(logger_section)

            logger = LoggerFactory.get_logger(name="core", config=log_config)
            container.register_instance(LoggerInterface, logger)

        # 3. Storage komponens létrehozása a konfiggal és loggerrel
        storage: Optional[StorageInterface] = None
        if storage_path:
            storage = FileStorage(base_path=storage_path)
            container.register_instance(StorageInterface, storage)

        # 4. Komponensek összekötése
        components = CoreComponents(
            config=config,
            logger=logger,
            storage=storage,
        )

        # 5. Komponensek validálása
        if not components.validate():
            if logger:
                logger.warning("Nem minden core komponens került inicializálásra")

        return components

    @staticmethod
    def create_with_container(container: DIContainer) -> CoreComponents:
        """Core komponensek létrehozása meglévő konténerből."""
        return CoreComponents(
            config=container.resolve(ConfigManagerInterface),
            logger=container.resolve(LoggerInterface),
            storage=container.resolve(StorageInterface),
        )

    @staticmethod
    def create_minimal() -> CoreComponents:
        """Minimális core komponens készlet létrehozása."""
        config = ConfigManagerFactory.get_manager("config.yml")
        log_config: Dict[str, Any] = {}
        if config:
            logger_section = config.get_section("logger")
            if isinstance(logger_section, dict):
                log_config = logger_section

        logger = LoggerFactory.get_logger(name="core", config=log_config)
        storage = FileStorage()

        return CoreComponents(
            config=config,
            logger=logger,
            storage=storage,
        )
