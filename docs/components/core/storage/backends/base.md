# core/storage/backends/base.py

Storage Backend Base Modul.

Ez a modul tartalmazza a tárolási backend-ek absztrakt alaposztályát,
amely definiálja a kötelező interfészt minden tárolási implementációhoz.

## Osztályok

### `DataFrameProtocol`

Protokoll a DataFrame-szerű objektumok típusozásához.

### `StorageBackend`

Absztrakt alaposztály a tárolási backend-ek számára.

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


## Függvények

### `columns`

Lekéri a DataFrame oszlopait.

### `__len__`

Visszaadja a DataFrame sorainak számát.

### `__init__`

Inicializálja a StorageBackend példányt.

        Args:
            name: A backend egyedi neve
            supported_formats: A támogatott fájlformátumok listája
            is_async: Logikai érték, amely jelzi, hogy a backend
                támogatja-e az aszinkron műveleteket

### `write`

DataFrame adatok írása a megadott elérési útra.

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

### `read`

DataFrame adatok olvasása a megadott elérési útról.

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

### `append`

DataFrame adatok hozzáfűzése egy meglévő fájlhoz.

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

### `supports_format`

Ellenőrzi, hogy a backend támogatja-e a megadott formátumot.

        Args:
            format_name: A formátum neve (pl. 'parquet', 'csv')

        Returns:
            True, ha a formátum támogatott, egyébként False

### `get_info`

Fájl információinak lekérdezése.

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

### `validate_data`

DataFrame érvényességének ellenőrzése.

        Args:
            data: Az ellenőrizendő DataFrame

        Returns:
            True, ha a DataFrame érvényes, egyébként False

### `__repr__`

A backend szöveges reprezentációja.


---

**Forrásfájl:** [`core/storage/backends/base.py`](../../../neural_ai/core/storage/backends/base.py)
