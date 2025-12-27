"""Pandas Storage Backend Modul.

Ez a modul tartalmazza a Pandas alapú tárolási backend implementációt,
amely a FastParquet-et használja a DataFrame-ek tárolásához.
A modul lazy importot használ a pandas és fastparquet csomagok számára.
"""

import os
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

from neural_ai.core.storage.backends.base import StorageBackend

if TYPE_CHECKING:
    import pandas as pd

if __name__ == "__main__":
    raise RuntimeError("Ez a modul nem futtatható közvetlenül.")


class PandasDataFrame:
    """Wrapper osztály a Pandas DataFrame köré lazy importtal.

    Ez az osztály biztosítja, hogy a pandas és fastparquet csomagok csak
    akkor töltődjön be, amikor az osztályt valóban használják.
    """

    def __init__(self) -> None:
        """Inicializálja a PandasDataFrame wrapper-t."""
        self._pandas: Any = None
        self._fastparquet: Any = None

    def _import_pandas(self) -> tuple[Any, Any]:
        """Lazy import a pandas és fastparquet csomagok számára."""
        if self._pandas is None:
            import fastparquet
            import pandas as pd

            self._pandas = pd
            self._fastparquet = fastparquet
        return self._pandas, self._fastparquet

    @property
    def pd(self) -> Any:
        """Pandas modul lekérdezése."""
        return self._import_pandas()[0]

    @property
    def fp(self) -> Any:
        """FastParquet modul lekérdezése."""
        return self._import_pandas()[1]


class PandasBackend(StorageBackend):
    """Pandas alapú tárolási backend FastParquet formátumhoz.

    Ez a backend a Pandas DataFrame-eket használja és a FastParquet-et
    a hatékony Parquet tároláshoz. Támogatja a chunkolást és aszinkron
    műveleteket, valamint a particionált tárolást.

    A backend lazy importot használ, így a pandas és fastparquet csomagok
    csak akkor töltődnek be, amikor az osztályt példányosítják.

    Attribútumok:
        name: 'pandas'
        supported_formats: ['parquet']
        is_async: True
    """

    def __init__(self) -> None:
        """Inicializálja a PandasBackend példányt.

        A lazy import miatt a pandas és fastparquet csomagok csak akkor
        töltődnek be, amikor az első műveletet végrehajtjuk.
        """
        super().__init__(name="pandas", supported_formats=["parquet"], is_async=True)
        self._pandas_wrapper = PandasDataFrame()
        self._initialized = False

    def _ensure_initialized(self) -> None:
        """Biztosítja, hogy a pandas csomag betöltődött."""
        if not self._initialized:
            self._pandas_wrapper._import_pandas()
            self._initialized = True

    def write(self, data: Any, path: str, **kwargs: dict[str, Any]) -> None:
        """DataFrame adatok írása Parquet formátumban FastParquet használatával.

        Args:
            data: A tárolandó Pandas DataFrame
            path: A cél elérési út (.parquet kiterjesztéssel)
            **kwargs: További konfigurációs paraméterek
                - compression: Tömörítési algoritmus (alapértelmezett: 'snappy')
                - partition_by: Particionálási oszlopok listája
                - schema: Adatséma definíció
                - index: Index mentése (alapértelmezett: False)

        Raises:
            ValueError: Ha az adatok érvénytelenek vagy az elérési út hibás
            FileNotFoundError: Ha a célkönyvtár nem létezik
            RuntimeError: Ha a tárolási művelet sikertelen
        """
        self._ensure_initialized()

        try:
            # Ellenőrzések
            if not self.validate_data(data):
                raise ValueError("Érvénytelen DataFrame adatok")

            if not path.endswith(".parquet"):
                raise ValueError("Az elérési útnak .parquet kiterjesztéssel kell rendelkeznie")

            # Célkönyvtár létrehozása, ha nem létezik
            path_obj = Path(path)
            path_obj.parent.mkdir(parents=True, exist_ok=True)

            # Konfigurációs paraméterek
            compression: str = kwargs.get("compression", "snappy")  # type: ignore
            partition_by: list[str] | None = kwargs.get("partition_by", None)  # type: ignore
            index: bool = kwargs.get("index", False)  # type: ignore

            # Pandas DataFrame konvertálás, ha szükséges
            if not isinstance(data, self._pandas_wrapper.pd.DataFrame):
                pd_df = self._pandas_wrapper.pd.DataFrame(data)
            else:
                pd_df = data

            # Írás FastParquet használatával
            if partition_by:
                # Particionált írás
                self._write_partitioned(pd_df, path, partition_by, compression, index)
            else:
                # Egyszerű írás
                self._pandas_wrapper.fp.write(
                    path, pd_df, compression=compression, write_index=index
                )

        except Exception as e:
            raise RuntimeError(f"A tárolási művelet sikertelen: {str(e)}") from e

    def _write_partitioned(
        self, df: "pd.DataFrame", path: str, partition_by: list[str], compression: str, index: bool
    ) -> None:
        """Particionált Parquet fájl írása.

        Args:
            df: A tárolandó DataFrame
            path: A cél elérési út
            partition_by: Particionálási oszlopok listája
            compression: Tömörítési algoritmus
            index: Index mentése
        """
        self._ensure_initialized()

        # FastParquet particionált írás
        self._pandas_wrapper.fp.write(
            path, df, compression=compression, write_index=index, partition_on=partition_by
        )

    def read(self, path: str, **kwargs: dict[str, Any]) -> "pd.DataFrame":
        """DataFrame adatok olvasása Parquet fájlból FastParquet használatával.

        Args:
            path: A forrás elérési út
            **kwargs: További konfigurációs paraméterek
                - columns: Csak ezen oszlopok betöltése
                - filters: Szűrők a partíciókra (pl. [('year', '=', 2023)])
                - chunk_size: Chunk méret chunkolás esetén

        Returns:
            A beolvasott Pandas DataFrame

        Raises:
            FileNotFoundError: Ha a forrásfájl nem létezik
            ValueError: Ha a fájlformátum nem támogatott
            RuntimeError: Ha az olvasási művelet sikertelen
        """
        self._ensure_initialized()

        try:
            if not os.path.exists(path):
                raise FileNotFoundError(f"A forrásfájl nem található: {path}")

            # Konfigurációs paraméterek
            columns: list[str] | None = kwargs.get("columns", None)  # type: ignore
            filters: list[tuple[Any, ...]] | None = kwargs.get("filters", None)  # type: ignore
            chunk_size: int | None = kwargs.get("chunk_size", None)  # type: ignore

            # Chunkolás vagy egyszeri betöltés
            if chunk_size:
                # Chunkolás implementációja
                return self._read_chunked(path, chunk_size, columns, filters)
            else:
                # Egyszeri betöltés FastParquet használatával
                parquet_file = self._pandas_wrapper.fp.ParquetFile(path)
                return parquet_file.to_pandas(columns=columns, filters=filters)

        except FileNotFoundError:
            raise
        except Exception as e:
            raise RuntimeError(f"Az olvasási művelet sikertelen: {str(e)}") from e

    def _read_chunked(
        self,
        path: str,
        chunk_size: int,
        columns: list[str] | None,
        filters: list[tuple[Any, ...]] | None,
    ) -> "pd.DataFrame":
        """Chunkoltan olvassa a Parquet fájlt.

        Args:
            path: A forrás elérési út
            chunk_size: Egy chunk mérete sorokban
            columns: Csak ezen oszlopok betöltése
            filters: Szűrők a partíciókra

        Returns:
            Az összes chunkból összefűzött DataFrame
        """
        self._ensure_initialized()

        # FastParquet segítségével chunkolás
        parquet_file = self._pandas_wrapper.fp.ParquetFile(path)

        chunks = []
        for chunk in parquet_file.iter_row_groups():
            # A chunk már egy DataFrame, nem kell to_pandas hívni
            df_chunk = chunk
            chunks.append(df_chunk)

            # Ha elértük a kívánt chunk méretet, álljunk le
            if len(df_chunk) >= chunk_size:
                break

        # Összefűzés
        if chunks:
            return self._pandas_wrapper.pd.concat(chunks, ignore_index=True)
        else:
            return self._pandas_wrapper.pd.DataFrame()

    def append(self, data: Any, path: str, **kwargs: dict[str, Any]) -> None:
        """DataFrame adatok hozzáfűzése egy meglévő Parquet fájlhoz.

        Ha a célfájl nem létezik, létrehozza azt. Ha létezik, hozzáfűzi
        az új adatokat a meglévőhöz.

        Args:
            data: A hozzáfűzendő DataFrame
            path: A cél elérési út
            **kwargs: További konfigurációs paraméterek
                - compression: Tömörítési algoritmus
                - schema_validation: Sémavizsgálat engedélyezése
                - index: Index mentése

        Raises:
            ValueError: Ha az adatok sémája nem kompatibilis a meglévővel
            FileNotFoundError: Ha a célkönyvtár nem létezik
            RuntimeError: Ha a hozzáfűzési művelet sikertelen
        """
        self._ensure_initialized()

        try:
            # Ellenőrzések
            if not self.validate_data(data):
                raise ValueError("Érvénytelen DataFrame adatok")

            # Pandas DataFrame konvertálás, ha szükséges
            if not isinstance(data, self._pandas_wrapper.pd.DataFrame):
                new_data = self._pandas_wrapper.pd.DataFrame(data)
            else:
                new_data = data

            # Ha a fájl létezik, olvassuk ki és fűzzük hozzá az új adatokat
            if os.path.exists(path):
                existing_data = self.read(path)

                # Sémavizsgálat, ha kérték
                if kwargs.get("schema_validation", False):
                    if not self._validate_schema(existing_data, new_data):
                        raise ValueError("Az adatok sémája nem kompatibilis a meglévővel")

                # Összefűzés
                combined_data = self._pandas_wrapper.pd.concat(
                    [existing_data, new_data], ignore_index=True
                )
            else:
                combined_data = new_data

            # Újraírás
            self.write(combined_data, path, **kwargs)

        except (ValueError, FileNotFoundError):
            raise
        except Exception as e:
            raise RuntimeError(f"A hozzáfűzési művelet sikertelen: {str(e)}") from e

    def _validate_schema(self, existing: "pd.DataFrame", new: "pd.DataFrame") -> bool:
        """Ellenőrzi, hogy a két DataFrame sémája kompatibilis-e.

        Args:
            existing: A meglévő DataFrame
            new: Az új DataFrame

        Returns:
            True, ha a sémák kompatibilisek, egyébként False
        """
        try:
            existing_cols = set(existing.columns)
            new_cols = set(new.columns)

            # Az új adatoknak tartalmazniuk kell az összes meglévő oszlopot
            return existing_cols.issubset(new_cols)
        except Exception:
            return False

    def supports_format(self, format_name: str) -> bool:
        """Ellenőrzi, hogy a backend támogatja-e a megadott formátumot.

        Args:
            format_name: A formátum neve (pl. 'parquet', 'csv')

        Returns:
            True, ha a formátum támogatott, egyébként False
        """
        return format_name.lower() in self.supported_formats

    def get_info(self, path: str) -> dict[str, Any]:
        """Parquet fájl információinak lekérdezése.

        Args:
            path: Az elérési út

        Returns:
            A fájl információit tartalmazó dictionary:
                - size: Fájlméret bájtban
                - rows: Sorok száma
                - columns: Oszlopok listája
                - format: 'parquet'
                - created: Létrehozás dátuma
                - modified: Módosítás dátuma

        Raises:
            FileNotFoundError: Ha a fájl nem létezik
        """
        self._ensure_initialized()

        try:
            if not os.path.exists(path):
                raise FileNotFoundError(f"A fájl nem található: {path}")

            # Fájl statisztikák
            stat = os.stat(path)

            # FastParquet fájl információk
            parquet_file = self._pandas_wrapper.fp.ParquetFile(path)
            metadata = parquet_file.info

            # DataFrame betöltése a sorok számának lekérdezéséhez
            df_sample = parquet_file.to_pandas()

            return {
                "size": stat.st_size,
                "rows": len(df_sample),
                "columns": list(df_sample.columns),
                "format": "parquet",
                "created": datetime.fromtimestamp(stat.st_ctime),
                "modified": datetime.fromtimestamp(stat.st_mtime),
                "num_row_groups": len(parquet_file.row_groups),
                "compression": metadata.get("compression", "unknown"),
            }

        except FileNotFoundError:
            raise
        except Exception as e:
            raise RuntimeError(f"Az információ lekérdezése sikertelen: {str(e)}") from e
