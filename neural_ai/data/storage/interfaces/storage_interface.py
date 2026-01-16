"""Storage interfész modul.

Ez a modul definiálja a tárolási műveletek absztrakt interfészét,
amelyet minden konkrét tárolási implementációnak implementálnia kell.
"""

from abc import ABC, abstractmethod
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import TYPE_CHECKING, Any

import pandas as pd

if TYPE_CHECKING:
    pass


class StorageInterface(ABC):
    """Absztrakt interfész tárolási műveletek definiálásához.

    Ez az interfész biztosítja a standardizált tárolási műveleteket
    DataFrame-ekkel és általános objektumokkal való munkavégzéshez.
    """

    @abstractmethod
    def save_dataframe(self, df: pd.DataFrame, path: str, **kwargs: Mapping[str, Any]) -> None:
        """DataFrame mentése a megadott útvonalra.

        Args:
            df: A mentendő pandas DataFrame.
            path: A célfájl elérési útja.
            **kwargs: További formázási és mentési opciók.

        Raises:
            StorageIOError: Ha I/O hiba történik a mentés során.
            StorageFormatError: Ha a kért formátum nem támogatott.
            StorageSerializationError: Ha az adatok nem szerializálhatók.
        """

    @abstractmethod
    def load_dataframe(self, path: str, **kwargs: Mapping[str, Any]) -> pd.DataFrame:
        """DataFrame betöltése a megadott útvonalról.

        Args:
            path: A forrásfájl elérési útja.
            **kwargs: További betöltési és formázási opciók.

        Returns:
            A betöltött pandas DataFrame.

        Raises:
            StorageNotFoundError: Ha a forrásfájl nem található.
            StorageFormatError: Ha a fájl formátuma nem támogatott.
            StorageSerializationError: Ha az adatok nem deszerializálhatók.
            StorageIOError: Ha I/O hiba történik a betöltés során.
        """

    @abstractmethod
    def save_object(self, obj: object, path: str, **kwargs: Mapping[str, Any]) -> None:
        """Objektum mentése a megadott útvonalra.

        Args:
            obj: A mentendő objektum.
            path: A célfájl elérési útja.
            **kwargs: További szerializációs opciók.

        Raises:
            StorageIOError: Ha I/O hiba történik a mentés során.
            StorageFormatError: Ha a kért formátum nem támogatott.
            StorageSerializationError: Ha az objektum nem szerializálható.
        """

    @abstractmethod
    def load_object(self, path: str, **kwargs: Mapping[str, Any]) -> object:
        """Objektum betöltése a megadott útvonalról.

        Args:
            path: A forrásfájl elérési útja.
            **kwargs: További deszerializációs opciók.

        Returns:
            A betöltött objektum.

        Raises:
            StorageNotFoundError: Ha a forrásfájl nem található.
            StorageFormatError: Ha a fájl formátuma nem támogatott.
            StorageSerializationError: Ha az objektum nem deszerializálható.
            StorageIOError: Ha I/O hiba történik a betöltés során.
        """

    @abstractmethod
    def exists(self, path: str) -> bool:
        """Ellenőrzi, hogy az útvonal létezik-e.

        Args:
            path: Az ellenőrizendő útvonal.

        Returns:
            True, ha az útvonal létezik, egyébként False.
        """

    @abstractmethod
    def get_metadata(self, path: str) -> dict[str, Any]:
        """Fájl vagy könyvtár metaadatainak lekérdezése.

        Args:
            path: A cél útvonal.

        Returns:
            A metaadatok szótárba rendezve.

        Raises:
            StorageNotFoundError: Ha az útvonal nem található.
            StorageIOError: Ha a metaadatok lekérdezése sikertelen.
        """

    @abstractmethod
    def delete(self, path: str) -> None:
        """Fájl vagy könyvtár törlése.

        Args:
            path: A törlendő útvonal.

        Raises:
            StorageNotFoundError: Ha az útvonal nem található.
            StorageIOError: Ha a törlés sikertelen.
        """

    @abstractmethod
    def list_dir(self, path: str, pattern: str | None = None) -> Sequence[Path]:
        """Könyvtár tartalmának listázása.

        Args:
            path: A könyvtár elérési útja.
            pattern: Opcionális glob minta a fájlnevek szűrésére.

        Returns:
            A könyvtárban található elemek Path objektumokként.

        Raises:
            StorageNotFoundError: Ha a könyvtár nem található.
            StorageIOError: Ha a listázás sikertelen.
        """
