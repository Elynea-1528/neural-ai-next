"""Storage factory interfész."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Optional, Type, Union

from neural_ai.core.storage.interfaces.storage_interface import StorageInterface


class StorageFactoryInterface(ABC):
    """Storage factory interfész."""

    @classmethod
    @abstractmethod
    def register_storage(cls, storage_type: str, storage_class: Type[StorageInterface]) -> None:
        """Új storage típus regisztrálása.

        Args:
            storage_type: A storage típus azonosítója
            storage_class: A storage osztály
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_storage(
        cls,
        storage_type: str = "file",
        base_path: Optional[Union[str, Path]] = None,
        **kwargs: Any,
    ) -> StorageInterface:
        """Storage példány létrehozása.

        Args:
            storage_type: A kért storage típus
            base_path: Alap könyvtár útvonal
            **kwargs: További paraméterek a storage-nak

        Returns:
            StorageInterface: Az inicializált storage
        """
        raise NotImplementedError
