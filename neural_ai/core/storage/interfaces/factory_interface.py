"""Storage factory interfész a különböző tárolási megoldások létrehozásához.

Ez az interfész egy gyártó (factory) mintát definiál, amely lehetővé teszi a tárolási
implementációk dinamikus regisztrálását és példányosítását. Az interfész segítségével
a rendszer függetlenítetté válik a konkrét tárolási osztályoktól.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from neural_ai.core.storage.interfaces.storage_interface import StorageInterface


class StorageFactoryInterface(ABC):
    """Storage factory interfész a tárolási implementációk gyártásához.

    Ez egy absztrakt alaposztály, amely meghatározza a tárolási factory-k
    alapvető viselkedését. A konkrét implementációknak ezt az interfészt kell
    megvalósítaniuk a saját factory osztályaikban.
    """

    @classmethod
    @abstractmethod
    def register_storage(
        cls,
        storage_type: str,
        storage_class: "type[StorageInterface]",
    ) -> None:
        """Új tárolási típus regisztrálása a factory számára.

        Args:
            storage_type: A tárolási típus egyedi azonosítója (pl. 'file', 's3').
            storage_class: A tárolási osztály, amely megvalósítja a StorageInterface-t.

        Raises:
            NotImplementedError: Ha az alosztály nem valósítja meg ezt a metódust.
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_storage(
        cls,
        storage_type: str = "file",
        base_path: str | Path | None = None,
        **kwargs: dict[str, object],
    ) -> "StorageInterface":
        """Tárolási példány létrehozása a megadott típus alapján.

        Args:
            storage_type: A kért tárolási típus azonosítója. Alapértelmezett: 'file'.
            base_path: Az alap könyvtár útvonala a fájl alapú tároláshoz.
            **kwargs: További, a tárolási implementáció specifikus paraméterek.

        Returns:
            StorageInterface: Egy inicializált tárolási példány.

        Raises:
            NotImplementedError: Ha az alosztály nem valósítja meg ezt a metódust.
            KeyError: Ha a megadott tárolási típus nincs regisztrálva.
            ValueError: Ha a megadott paraméterek érvénytelenek.
        """
        raise NotImplementedError
