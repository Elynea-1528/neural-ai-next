"""Adattárolási factory implementáció a különböző tároló komponensek létrehozásához.

Ez a modul felelős a tárolási implementációk példányosításáért a factory
minta segítségével. Alapértelmezetten a FileStorage implementációt támogatja,
de további tárolási típusok is regisztrálhatók dinamikusan.
"""

from pathlib import Path
from typing import TYPE_CHECKING

from neural_ai.core.config.factory import ConfigManagerFactory
from neural_ai.core.config.interfaces.types import StorageConfig
from neural_ai.core.events.factory import EventBusFactory
from neural_ai.core.logger.factory import LoggerFactory
from neural_ai.data.storage.exceptions import StorageError
from neural_ai.data.storage.implementations.file_storage import FileStorage
from neural_ai.data.storage.implementations.parquet_storage import (
    ParquetStorageService,
)
from neural_ai.data.storage.interfaces.factory_interface import StorageFactoryInterface
from neural_ai.data.storage.interfaces.storage_interface import StorageInterface

if TYPE_CHECKING:
    from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
    from neural_ai.core.events.interfaces.event_bus_interface import EventBusInterface
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
    from neural_ai.core.utils.interfaces.hardware_interface import HardwareInterface


class StorageFactory(StorageFactoryInterface):
    """Factory osztály tárolási komponensek létrehozásához.

    Ez az osztály felelős a különböző tárolási implementációk példányosításáért.
    Alapértelmezetten a FileStorage implementációt támogatja, de további
    tárolási típusok is regisztrálhatók.
    """

    _storage_types: dict[str, type[StorageInterface]] = {
        "file": FileStorage,
        "parquet": ParquetStorageService,
    }

    @classmethod
    def register_storage(cls, storage_type: str, storage_class: type[StorageInterface]) -> None:
        """Új tárolási típus regisztrálása a factory számára.

        Args:
            storage_type: A tárolási típus egyedi azonosítója (pl. "s3", "database").
            storage_class: A tárolási osztály, amely implementálja a StorageInterface-t.

        Raises:
            ValueError: Ha a storage_class nem implementálja a StorageInterface-t.

        Example:
            >>> from neural_ai.data.storage.interfaces import StorageInterface
            >>> class S3Storage(StorageInterface):
            ...     pass
            >>> StorageFactory.register_storage("s3", S3Storage)
        """
        cls._storage_types[storage_type] = storage_class

    @classmethod
    def get_registered_types(cls) -> dict[str, type[StorageInterface]]:
        """Visszaadja a regisztrált tárolási típusokat.

        Returns:
            A regisztrált tárolási típusok szótára.
        """
        return cls._storage_types.copy()

    @classmethod
    def get_storage(
        cls,
        logger: "LoggerInterface | None" = None,
        config: "ConfigManagerInterface | None" = None,
        event_bus: "EventBusInterface | None" = None,
        storage_type: str = "file",
        base_path: str | Path | None = None,
        hardware: "HardwareInterface | None" = None,
        **kwargs: object,
    ) -> StorageInterface:
        """Tárolási példány létrehozása a megadott típus alapján.

        Args:
            logger: A naplózásért felelős interfész.
            config: A konfigurációért felelős interfész.
            event_bus: Az eseménybusz interfész.
            storage_type: A kért tárolási típus azonosítója (alapértelmezett: "file").
            base_path: Alap könyvtár útvonal a fájl alapú tároláshoz.
            hardware: A hardverképességek detektálásáért felelős interfész (opcionális).
            **kwargs: További paraméterek a tárolási osztály konstruktorának.

        Returns:
            StorageInterface: Az inicializált tárolási példány.

        Raises:
            StorageError: Ha nem található a kért tárolási típus vagy a
                példányosítása sikertelen.

        Example:
            >>> storage = StorageFactory.get_storage(logger_instance, "file", base_path="data")
            >>> storage.save_object({"key": "value"}, "config.json")
            >>> # Egyéni paraméterekkel
            >>> storage = StorageFactory.get_storage(logger_instance, "file", base_path="data",
            ...                                       create_if_missing=True)
        """
        if storage_type not in cls._storage_types:
            raise StorageError(
                f"Ismeretlen storage típus: {storage_type}. "
                f"Elérhető típusok: {list(cls._storage_types.keys())}"
            )

        storage_class = cls._storage_types[storage_type]

        # A base_path hozzáadása a kwargs-hoz, ha meg van adva
        if base_path is not None:
            kwargs["base_path"] = base_path

        # A hardware hozzáadása a kwargs-hoz, ha meg van adva
        if hardware is not None:
            kwargs["hardware"] = hardware

        # Logger hozzáadása a kwargs-hoz
        if logger is None:
            logger = LoggerFactory.get_logger(__name__)
        kwargs["logger"] = logger

        # Config hozzáadása a kwargs-hoz
        if config is None:
            config = ConfigManagerFactory.get_manager("configs/storage.yaml")
        kwargs["config"] = config

        # Config validáció Pydantic-kal
        raw_config = config.get("storage")
        try:
            storage_conf = StorageConfig(**(raw_config if isinstance(raw_config, dict) else {}))
            logger.debug(
                "Storage config validation completed", storage_config=storage_conf.model_dump()
            )
        except Exception as e:
            logger.error("Storage config validation failed", error=str(e))
            raise StorageError(f"Érvénytelen storage konfiguráció: {e}") from e

        # EventBus hozzáadása a kwargs-hoz
        if event_bus is None:
            event_bus_factory = EventBusFactory(logger, config)
            event_bus = event_bus_factory.create()
        kwargs["event_bus"] = event_bus

        try:
            logger.debug(
                "Creating storage instance",
                storage_type=storage_type,
                storage_class=str(storage_class),
            )
            storage = storage_class(**kwargs)
            logger.info("Storage instance created successfully", storage_type=storage_type)
            return storage
        except TypeError as e:
            logger.error(
                "Failed to create storage instance due to type error",
                storage_type=storage_type,
                error=str(e),
            )
            raise StorageError(f"Nem sikerült létrehozni a storage példányt: {str(e)}") from e
        except Exception as e:
            logger.error(
                "Unexpected error during storage instantiation",
                storage_type=storage_type,
                error=str(e),
            )
            raise StorageError(
                f"Váratlan hiba történt a storage példányosítása közben: {str(e)}"
            ) from e
