"""Storage interfész modul."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Optional, Sequence

import pandas as pd


class StorageInterface(ABC):
    """Storage interfész osztály."""

    @abstractmethod
    def save_dataframe(self, df: pd.DataFrame, path: str, **kwargs: Any) -> None:
        """Végrehajt egy DataFrame mentési műveletet.

        Args:
            df: A mentendő DataFrame
            path: A mentés útvonala
            **kwargs: További paraméterek

        Raises:
            StorageIOError: Ha a mentés sikertelen
            StorageFormatError: Ha a formátum nem támogatott
            StorageSerializationError: Ha az adatok nem szerializálhatók
        """

    @abstractmethod
    def load_dataframe(self, path: str, **kwargs: Any) -> pd.DataFrame:
        """Betölt egy DataFrame objektumot a megadott útvonalon.

        Args:
            path: A betöltendő fájl útvonala
            **kwargs: További paraméterek

        Returns:
            pd.DataFrame: A betöltött DataFrame

        Raises:
            StorageNotFoundError: Ha a fájl nem található
            StorageFormatError: Ha a formátum nem támogatott
            StorageSerializationError: Ha az adatok nem deszerializálhatók
            StorageIOError: Ha a betöltés sikertelen
        """

    @abstractmethod
    def save_object(self, obj: Any, path: str, **kwargs: Any) -> None:
        """Végrehajt egy objektum mentési műveletet.

        Args:
            obj: A mentendő objektum
            path: A mentés útvonala
            **kwargs: További paraméterek

        Raises:
            StorageIOError: Ha a mentés sikertelen
            StorageFormatError: Ha a formátum nem támogatott
            StorageSerializationError: Ha az objektum nem szerializálható
        """

    @abstractmethod
    def load_object(self, path: str, **kwargs: Any) -> Any:
        """Betölt egy objektumot a megadott útvonalon.

        Args:
            path: A betöltendő fájl útvonala
            **kwargs: További paraméterek

        Returns:
            Any: A betöltött objektum

        Raises:
            StorageNotFoundError: Ha a fájl nem található
            StorageFormatError: Ha a formátum nem támogatott
            StorageSerializationError: Ha az objektum nem deszerializálható
            StorageIOError: Ha a betöltés sikertelen
        """

    @abstractmethod
    def exists(self, path: str) -> bool:
        """Ellenőrzi egy útvonal létezését.

        Args:
            path: Az ellenőrizendő útvonal

        Returns:
            bool: True, ha létezik, False ha nem
        """

    @abstractmethod
    def get_metadata(self, path: str) -> Dict[str, Any]:
        """Lekéri egy fájl vagy könyvtár metaadatait.

        Args:
            path: A fájl vagy könyvtár útvonala

        Returns:
            Dict[str, Any]: A metaadatok

        Raises:
            StorageNotFoundError: Ha a fájl nem található
            StorageIOError: Ha a lekérés sikertelen
        """

    @abstractmethod
    def delete(self, path: str) -> None:
        """Törli a megadott fájlt vagy könyvtárat.

        Args:
            path: A törlendő útvonal

        Raises:
            StorageNotFoundError: Ha a fájl nem található
            StorageIOError: Ha a törlés sikertelen
        """

    @abstractmethod
    def list_dir(self, path: str, pattern: Optional[str] = None) -> Sequence[Path]:
        """Listázza egy könyvtár tartalmát.

        Args:
            path: A könyvtár útvonala
            pattern: Szűrő minta a fájlnevekre

        Returns:
            Sequence[Path]: A könyvtár tartalma Path objektumokként

        Raises:
            StorageNotFoundError: Ha a könyvtár nem található
            StorageIOError: Ha a listázás sikertelen
        """
