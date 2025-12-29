# core/storage/backends/polars_backend.py

Polars Storage Backend Modul.

Ez a modul tartalmazza a Polars alapú tárolási backend implementációt,
amely a Parquet formátumot használja a DataFrame-ek tárolásához.
A modul lazy importot használ a polars és pyarrow csomagok számára.

## Osztályok

### `PolarsDataFrame`

Wrapper osztály a Polars DataFrame köré lazy importtal.

    Ez az osztály biztosítja, hogy a polars csomag csak akkor töltődjön be,
    amikor az osztályt valóban használják.

### `PolarsBackend`

Polars alapú tárolási backend Parquet formátumhoz.

    Ez a backend a Polars DataFrame-eket használja a gyors adatfeldolgozáshoz
    és a PyArrow Parquet formátumot a hatékony tároláshoz. Támogatja a
    chunkolást, aszinkron műveleteket és a particionált tárolást.

    A backend lazy importot használ, így a polars és pyarrow csomagok csak
    akkor töltődnek be, amikor az osztályt példányosítják.

    Attribútumok:
        name: 'polars'
        supported_formats: ['parquet']
        is_async: True


## Függvények

### `__init__`

Inicializálja a PolarsBackend példányt.

        A lazy import miatt a polars és pyarrow csomagok csak akkor
        töltődnek be, amikor az első műveletet végrehajtjuk.

### `_import_polars`

Lazy import a polars és pyarrow csomagok számára.

### `pl`

Polars modul lekérdezése.

### `pa`

PyArrow modul lekérdezése.

### `pq`

PyArrow Parquet modul lekérdezése.

### `_ensure_initialized`

Biztosítja, hogy a polars csomag betöltődött.

### `write`

DataFrame adatok írása Parquet formátumban.

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

### `read`

DataFrame adatok olvasása Parquet fájlból.

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

**Forrásfájl:** [`core/storage/backends/polars_backend.py`](../../../neural_ai/core/storage/backends/polars_backend.py)
