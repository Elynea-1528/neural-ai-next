"""Storage factory implementáció."""

from pathlib import Path
from typing import Any

from neural_ai.core.storage.exceptions import StorageError
from neural_ai.core.storage.implementations.file_storage import FileStorage
from neural_ai.core.storage.interfaces.factory_interface import StorageFactoryInterface
from neural_ai.core.storage.interfaces.storage_interface import StorageInterface


class StorageFactory(StorageFactoryInterface):
    """Factory osztály storage komponensek létrehozásához.

    Ez az osztály felelős a különböző storage implementációk példányosításáért.
    Alapértelmezetten a FileStorage implementációt támogatja, de további
    storage típusok is regisztrálhatók.
    """

    _storage_types: dict[str, type[StorageInterface]] = {
        "file": FileStorage,
    }

    @classmethod
    def register_storage(cls, storage_type: str, storage_class: type[StorageInterface]) -> None:
        """Új storage típus regisztrálása.

        Args:
            storage_type: A storage típus azonosítója
            storage_class: A storage osztály

        Example:
            >>> StorageFactory.register_storage("s3", S3Storage)
        """
        cls._storage_types[storage_type] = storage_class

    @classmethod
    def get_storage(
        cls,
        storage_type: str = "file",
        base_path: str | Path | None = None,
        **kwargs: Any,
    ) -> StorageInterface:
        """Storage példány létrehozása.

        Args:
            storage_type: A kért storage típus
            base_path: Alap könyvtár útvonal
            **kwargs: További paraméterek a storage-nak

        Returns:
            StorageInterface: Az inicializált storage

        Raises:
            StorageError: Ha nem található a kért storage típus

        Example:
            >>> storage = StorageFactory.get_storage("file", base_path="data")
            >>> storage.save_object({"key": "value"}, "config.json")
        """
        if storage_type not in cls._storage_types:
            raise StorageError(
                f"Ismeretlen storage típus: {storage_type}. "
                f"Elérhető típusok: {list(cls._storage_types.keys())}"
            )

        storage_class = cls._storage_types[storage_type]

        # A **kwargs-ban továbbítjuk az összes paramétert, beleértve a base_path-t is
        if base_path is not None:
            kwargs["base_path"] = base_path

        try:
            storage = storage_class(**kwargs)
            return storage
        except TypeError as e:
            raise StorageError(f"Nem sikerült létrehozni a storage példányt: {str(e)}")
