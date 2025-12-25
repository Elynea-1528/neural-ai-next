"""Polars Storage Backend Modul.

Ez a modul tartalmazza a Polars alapú tárolási backend implementációt,
amely a Parquet formátumot használja a DataFrame-ek tárolásához.
A modul lazy importot használ a polars és pyarrow csomagok számára.
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Any

from neural_ai.core.storage.backends.base import StorageBackend

if __name__ == "__main__":
    raise RuntimeError("Ez a modul nem futtatható közvetlenül.")

# Modul szintű változók a lazy import támogatásához
# Ezeket a tesztelés során lehet mock-olni
polars = None
pyarrow = None
pq = None


class PolarsDataFrame:
    """Wrapper osztály a Polars DataFrame köré lazy importtal.

    Ez az osztály biztosítja, hogy a polars csomag csak akkor töltődjön be,
    amikor az osztályt valóban használják.
    """

    def __init__(self):
        """Inicializálja a PolarsDataFrame wrapper-t."""
        self._polars = None
        self._pyarrow = None

    def _import_polars(self):
        """Lazy import a polars és pyarrow csomagok számára."""
        if self._polars is None:
            import polars as pl
            import pyarrow as pa
            import pyarrow.parquet as pq

            self._polars = pl
            self._pyarrow = pa
            self._parquet = pq
            
            # Frissítsük a modul szintű változókat is a teszteléshez
            import neural_ai.core.storage.backends.polars_backend as pb_module
            pb_module.polars = pl
            pb_module.pyarrow = pa
            pb_module.pq = pq
        return self._polars, self._pyarrow, self._parquet

    @property
    def pl(self):
        """Polars modul lekérdezése."""
        return self._import_polars()[0]

    @property
    def pa(self):
        """PyArrow modul lekérdezése."""
        return self._import_polars()[1]

    @property
    def pq(self):
        """PyArrow Parquet modul lekérdezése."""
        return self._import_polars()[2]


class PolarsBackend(StorageBackend):
    """Polars alapú tárolási backend Parquet formátumhoz.

    Ez a backend a Polars DataFrame-eket használja a gyors adatfeldolgozáshoz
    és a PyArrow Parquet formátumot a hatékony tároláshoz. Támogatja a
    chunkolást, aszinkron műveleteket és a particionált tárolást.

    A backend lazy importot használ, így a polars és pyarrow csomagok csak
    akkor töltődnek be, amikor az osztályt példányosítják.

    Attribútumok:
        name: 'polars'
        supported_formats: ['parquet']
        is_async: True
    """

    def __init__(self):
        """Inicializálja a PolarsBackend példányt.

        A lazy import miatt a polars és pyarrow csomagok csak akkor
        töltődnek be, amikor az első műveletet végrehajtjuk.
        """
        super().__init__(name="polars", supported_formats=["parquet"], is_async=True)
        self._polars_wrapper = PolarsDataFrame()
        self._initialized = False

    def _ensure_initialized(self):
        """Biztosítja, hogy a polars csomag betöltődött."""
        if not self._initialized:
            self._polars_wrapper._import_polars()
            self._initialized = True

    def write(self, data: Any, path: str, **kwargs: dict[str, Any]) -> None:
        """DataFrame adatok írása Parquet formátumban.

        Args:
            data: A tárolandó Polars DataFrame
            path: A cél elérési út (.parquet kiterjesztéssel)
            **kwargs: További konfigurációs paraméterek
                - compression: Tömörítési algoritmus (alapértelmezett: 'snappy')
                - partition_by: Particionálási oszlopok listája
                - schema: Adatséma definíció

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
            compression = kwargs.get("compression", "snappy")
            partition_by = kwargs.get("partition_by", None)

            # Polars DataFrame konvertálás, ha szükséges
            if not isinstance(data, self._polars_wrapper.pl.DataFrame):
                pl_df = self._polars_wrapper.pl.DataFrame(data)
            else:
                pl_df = data

            # Írás particionálással vagy anélkül
            if partition_by:
                pl_df.write_parquet(
                    path,
                    compression=compression,
                    use_pyarrow=True,
                    pyarrow_options={"partition_by": partition_by},
                )
            else:
                pl_df.write_parquet(path, compression=compression)

        except Exception as e:
            raise RuntimeError(f"A tárolási művelet sikertelen: {str(e)}") from e

    def read(self, path: str, **kwargs: dict[str, Any]) -> Any:
        """DataFrame adatok olvasása Parquet fájlból.

        Args:
            path: A forrás elérési út
            **kwargs: További konfigurációs paraméterek
                - columns: Csak ezen oszlopok betöltése
                - filters: Szűrők a partíciókra (pl. [('year', '=', 2023)])
                - chunk_size: Chunk méret chunkolás esetén

        Returns:
            A beolvasott Polars DataFrame

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
            columns = kwargs.get("columns", None)
            filters = kwargs.get("filters", None)
            chunk_size = kwargs.get("chunk_size", None)

            # Chunkolás vagy egyszeri betöltés
            if chunk_size:
                # Chunkolás implementációja
                return self._read_chunked(path, chunk_size, columns, filters)
            else:
                # Egyszeri betöltés
                return self._polars_wrapper.pl.read_parquet(
                    path,
                    columns=columns,
                    use_pyarrow=True,
                    pyarrow_options={"filters": filters} if filters else None,
                )

        except FileNotFoundError:
            raise
        except Exception as e:
            raise RuntimeError(f"Az olvasási művelet sikertelen: {str(e)}") from e

    def _read_chunked(
        self, path: str, chunk_size: int, columns: list | None, filters: list | None
    ) -> Any:
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

        # PyArrow segítségével chunkolás
        parquet_file = self._polars_wrapper.pq.ParquetFile(path)

        chunks = []
        for batch in parquet_file.iter_batches(
            batch_size=chunk_size, columns=columns, filters=filters
        ):
            chunks.append(self._polars_wrapper.pl.from_arrow(batch))

        # Összefűzés
        if chunks:
            return self._polars_wrapper.pl.concat(chunks)
        else:
            return self._polars_wrapper.pl.DataFrame()

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

            # Polars DataFrame konvertálás, ha szükséges
            if not isinstance(data, self._polars_wrapper.pl.DataFrame):
                new_data = self._polars_wrapper.pl.DataFrame(data)
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
                combined_data = self._polars_wrapper.pl.concat([existing_data, new_data])
            else:
                combined_data = new_data

            # Újraírás
            self.write(combined_data, path, **kwargs)

        except (ValueError, FileNotFoundError):
            raise
        except Exception as e:
            raise RuntimeError(f"A hozzáfűzési művelet sikertelen: {str(e)}") from e

    def _validate_schema(self, existing: Any, new: Any) -> bool:
        """Ellenőrzi, hogy a két DataFrame sémája kompatibilis-e.

        Args:
            existing: A meglévő DataFrame
            new: Az új DataFrame

        Returns:
            True, ha a sémák kompatibilisek, egyébként False
        """
        try:
            # Lekérjük az oszlopokat (attribútum vagy metódus)
            existing_cols = None
            new_cols = None
            
            if hasattr(existing, 'columns') and callable(existing.columns):
                existing_cols = set(existing.columns())
            elif hasattr(existing, 'columns'):
                existing_cols = set(existing.columns)
                
            if hasattr(new, 'columns') and callable(new.columns):
                new_cols = set(new.columns())
            elif hasattr(new, 'columns'):
                new_cols = set(new.columns)

            # Ha valamelyik oszlophalmaz None, akkor nem kompatibilis
            if existing_cols is None or new_cols is None:
                return False

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

            # Parquet fájl információk
            parquet_file = self._polars_wrapper.pq.ParquetFile(path)
            metadata = parquet_file.metadata

            return {
                "size": stat.st_size,
                "rows": metadata.num_rows,
                "columns": list(metadata.schema.names),
                "format": "parquet",
                "created": datetime.fromtimestamp(stat.st_ctime),
                "modified": datetime.fromtimestamp(stat.st_mtime),
                "num_row_groups": metadata.num_row_groups,
                "compression": metadata.row_group(0).column(0).compression,
            }

        except FileNotFoundError:
            raise
        except Exception as e:
            raise RuntimeError(f"Az információ lekérdezése sikertelen: {str(e)}") from e
