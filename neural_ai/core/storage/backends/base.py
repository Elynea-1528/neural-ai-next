"""Storage Backend Base Modul.

Ez a modul tartalmazza a tárolási backend-ek absztrakt alaposztályát,
amely definiálja a kötelező interfészt minden tárolási implementációhoz.
"""

from abc import ABC, abstractmethod
from typing import Any, Protocol

if __name__ == "__main__":
    raise RuntimeError("Ez a modul nem futtatható közvetlenül.")


class DataFrameType(Protocol):
    """DataFrame protokoll, amely definiálja a kötelező DataFrame műveleteket."""

    def __len__(self) -> int:
        """DataFrame hosszának lekérdezése."""
        ...

    def columns(self) -> list[str]:
        """Oszlopok lekérdezése."""
        ...

    def shape(self) -> tuple[int, int]:
        """DataFrame alakjának lekérdezése."""
        ...


class StorageBackend(ABC):
    """Absztrakt alaposztály a tárolási backend-ek számára.

    Ez az osztály definiálja a kötelező interfészt, amelyet minden tárolási
    backend implementációjának támogatnia kell. A backend-ek felelősek a
    DataFrame-ek tárolásáért, olvasásáért és hozzáfűzéséért különböző
    formátumokban (elsősorban Parquet).

    A backend-eknek támogatniuk kell a chunkolást és aszinkron műveleteket
    a nagy adathalmazok hatékony kezeléséhez.

    Attribútumok:
        name: A backend neve (pl. 'polars', 'pandas')
        supported_formats: A támogatott fájlformátumok listája
        is_async: Logikai érték, amely jelzi, hogy a backend támogatja-e az aszinkron műveleteket
    """

    def __init__(self, name: str, supported_formats: list[str], is_async: bool = True):
        """Inicializálja a StorageBackend példányt.

        Args:
            name: A backend egyedi neve
            supported_formats: A támogatott fájlformátumok listája
            is_async: Logikai érték, amely jelzi, hogy a backend
                támogatja-e az aszinkron műveleteket
        """
        self.name: str = name
        self.supported_formats: list[str] = supported_formats
        self.is_async: bool = is_async

    @abstractmethod
    def write(self, data: DataFrameType, path: str, **kwargs: dict[str, Any]) -> None:
        """DataFrame adatok írása a megadott elérési útra.

        Args:
            data: A tárolandó DataFrame
            path: A cél elérési út
            **kwargs: További konfigurációs paraméterek
                - compression: Tömörítési algoritmus (pl. 'snappy', 'gzip')
                - partition_by: Particionálási oszlopok listája
                - schema: Adatséma definíció

        Raises:
            ValueError: Ha az adatok érvénytelenek vagy az elérési út nem létezik
            FileNotFoundError: Ha a célkönyvtár nem létezik
            RuntimeError: Ha a tárolási művelet sikertelen
        """
        pass

    @abstractmethod
    def read(self, path: str, **kwargs: dict[str, Any]) -> DataFrameType:
        """DataFrame adatok olvasása a megadott elérési útról.

        Args:
            path: A forrás elérési út
            **kwargs: További konfigurációs paraméterek
                - columns: Csak ezen oszlopok betöltése
                - filters: Szűrők a partíciókra (pl. [('year', '=', 2023)])
                - chunk_size: Chunk méret chunkolás esetén

        Returns:
            A beolvasott DataFrame

        Raises:
            FileNotFoundError: Ha a forrásfájl nem létezik
            ValueError: Ha a fájlformátum nem támogatott
            RuntimeError: Ha az olvasási művelet sikertelen
        """
        pass

    @abstractmethod
    def append(self, data: DataFrameType, path: str, **kwargs: dict[str, Any]) -> None:
        """DataFrame adatok hozzáfűzése egy meglévő fájlhoz.

        Ha a célfájl nem létezik, létrehozza azt. Ha létezik, hozzáfűzi
        az új adatokat a meglévőhöz.

        Args:
            data: A hozzáfűzendő DataFrame
            path: A cél elérési út
            **kwargs: További konfigurációs paraméterek
                - compression: Tömörítési algoritmus
                - schema_validation: Sémavizsgálat engedélyezése

        Raises:
            ValueError: Ha az adatok sémája nem kompatibilis a meglévővel
            FileNotFoundError: Ha a célkönyvtár nem létezik
            RuntimeError: Ha a hozzáfűzési művelet sikertelen
        """
        pass

    @abstractmethod
    def supports_format(self, format_name: str) -> bool:
        """Ellenőrzi, hogy a backend támogatja-e a megadott formátumot.

        Args:
            format_name: A formátum neve (pl. 'parquet', 'csv')

        Returns:
            True, ha a formátum támogatott, egyébként False
        """
        pass

    @abstractmethod
    def get_info(self, path: str) -> dict[str, Any]:
        """Fájl információinak lekérdezése.

        Args:
            path: Az elérési út

        Returns:
            A fájl információit tartalmazó dictionary:
                - size: Fájlméret bájtban
                - rows: Sorok száma
                - columns: Oszlopok listája
                - format: Fájlformátum
                - created: Létrehozás dátuma
                - modified: Módosítás dátuma

        Raises:
            FileNotFoundError: Ha a fájl nem létezik
        """
        pass

    def validate_data(self, data: DataFrameType) -> bool:
        """DataFrame érvényességének ellenőrzése.

        Args:
            data: Az ellenőrizendő DataFrame

        Returns:
            True, ha a DataFrame érvényes, egyébként False
        """
        try:
            return len(data) >= 0 and len(data.columns()) > 0
        except Exception:
            return False

    def __repr__(self) -> str:
        """A backend szöveges reprezentációja."""
        return (
            f"{self.__class__.__name__}(name='{self.name}', "
            f"formats={self.supported_formats}, async={self.is_async})"
        )
