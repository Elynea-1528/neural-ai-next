# core/storage/backends/pandas_backend.py

Pandas Storage Backend Modul.

Ez a modul tartalmazza a Pandas alapú tárolási backend implementációt,
amely a FastParquet-et használja a DataFrame-ek tárolásához.
A modul lazy importot használ a pandas és fastparquet csomagok számára.

## Osztályok

### `PandasDataFrame`

Wrapper osztály a Pandas DataFrame köré lazy importtal.

    Ez az osztály biztosítja, hogy a pandas és fastparquet csomagok csak
    akkor töltődjön be, amikor az osztályt valóban használják.

### `PandasBackend`

Pandas alapú tárolási backend FastParquet formátumhoz.

    Ez a backend a Pandas DataFrame-eket használja és a FastParquet-et
    a hatékony Parquet tároláshoz. Támogatja a chunkolást és aszinkron
    műveleteket, valamint a particionált tárolást.

    A backend lazy importot használ, így a pandas és fastparquet csomagok
    csak akkor töltődnek be, amikor az osztályt példányosítják.

    Attribútumok:
        name: 'pandas'
        supported_formats: ['parquet']
        is_async: True


## Függvények

### `__init__`

Inicializálja a PandasBackend példányt.

        A lazy import miatt a pandas és fastparquet csomagok csak akkor
        töltődnek be, amikor az első műveletet végrehajtjuk.

### `_import_pandas`

Lazy import a pandas és fastparquet csomagok számára.

### `pd`

Pandas modul lekérdezése.

### `fp`

FastParquet modul lekérdezése.

### `_ensure_initialized`

Biztosítja, hogy a pandas csomag betöltődött.

### `write`

DataFrame adatok írása Parquet formátumban FastParquet használatával.

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

### `_write_partitioned`

Particionált Parquet fájl írása.

        Args:
            df: A tárolandó DataFrame
            path: A cél elérési út
            partition_by: Particionálási oszlopok listája
            compression: Tömörítési algoritmus
            index: Index mentése

### `read`

DataFrame adatok olvasása Parquet fájlból FastParquet használatával.

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

### `_read_chunked`

Chunkoltan olvassa a Parquet fájlt.

        Args:
            path: A forrás elérési út
            chunk_size: Egy chunk mérete sorokban
            columns: Csak ezen oszlopok betöltése
            filters: Szűrők a partíciókra

        Returns:
            Az összes chunkból összefűzött DataFrame

### `append`

DataFrame adatok hozzáfűzése egy meglévő Parquet fájlhoz.

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

### `_validate_schema`

Ellenőrzi, hogy a két DataFrame sémája kompatibilis-e.

        Args:
            existing: A meglévő DataFrame
            new: Az új DataFrame

        Returns:
            True, ha a sémák kompatibilisek, egyébként False

### `supports_format`

Ellenőrzi, hogy a backend támogatja-e a megadott formátumot.

        Args:
            format_name: A formátum neve (pl. 'parquet', 'csv')

        Returns:
            True, ha a formátum támogatott, egyébként False

### `get_info`

Parquet fájl információinak lekérdezése.

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


---

**Forrásfájl:** [`core/storage/backends/pandas_backend.py`](../../../neural_ai/core/storage/backends/pandas_backend.py)
