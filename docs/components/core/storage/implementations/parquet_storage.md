# core/storage/implementations/parquet_storage.py

ParquetStorageService - Particionált Parquet tároló szolgáltatás.

Ez a modul implementálja a Tick adatok particionált Parquet formátumban történő tárolását
és lekérdezését a Neural AI Next rendszer számára. A tárolás dátum és szimbólum alapú
particionálást használ a gyors lekérdezés érdekében.

A szolgáltatás hardver-gyorsítást detektál és automatikusan kiválasztja a legoptimálisabb
backend-et (PolarsBackend AVX2 támogatással, vagy PandasBackend kompatibilitási módban).

Author: Neural AI Next Team
Version: 2.0.0

## Osztályok

### `ParquetStorageService`

Particionált Parquet tároló szolgáltatás backend selectorral.

    Ez az osztály felelős a Tick adatok particionált Parquet formátumban történő
    tárolásáért és lekérdezéséért. A particionálás dátum és szimbólum alapú,
    ami lehetővé teszi a gyors és hatékony adatlekérdezést.

    A szolgáltatás automatikusan detektálja a hardver képességeket és kiválasztja
    a legoptimálisabb tárolási backend-et:
    - PolarsBackend: AVX2 támogatással gyorsabb feldolgozás
    - PandasBackend: Kompatibilitási mód régebbi CPU-khoz

    Attributes:
        BASE_PATH: A tárolás alapútvonala
        engine: A Parquet engine ('fastparquet' vagy 'polars')
        compression: Tömörítési algoritmus ('snappy')
        backend: A kiválasztott tárolási backend


## Függvények

### `__init__`

Inicializálja a ParquetStorageService-t backend selectorral.

        A hardver detekció alapján kiválasztja a megfelelő tárolási backend-et.
        Ha az AVX2 utasításkészlet elérhető, a PolarsBackend-et használja,
        egyébként a PandasBackend-et kompatibilitási módban.

        Args:
            base_path: Az alapútvonal a tároláshoz (opcionális)
            compression: A tömörítési algoritmus (alapértelmezett: 'snappy')
            hardware: A hardverképességek detektálásáért felelős interfész (opcionális)
            logger: A naplózásért felelős interfész (opcionális)
            **kwargs: További opcionális paraméterek

### `_select_backend`

Backend kiválasztása hardver detekció alapján.

        Ez a metódus felelős a megfelelő tárolási backend kiválasztásáért
        a hardver képességek alapján. Külön metódusba van kiszervezve,
        hogy a tesztek könnyen mockolhassák.

### `_get_path`

Elérési út generálása a megadott szimbólumhoz és dátumhoz.

        Args:
            symbol: A pénzpár szimbóluma (pl. 'EURUSD')
            date: A dátum

        Returns:
            A teljes elérési út a Parquet fájlhoz

        Example:
            >>> service = ParquetStorageService()
            >>> date = datetime(2023, 12, 23)
            >>> path = service._get_path('EURUSD', date)
            >>> print(path)
            /data/tick/EURUSD/tick/year=2023/month=12/day=23/data.parquet

### `store_tick_data`

Tick adatok tárolása particionált Parquet formátumban.

        Args:
            symbol: A pénzpár szimbóluma
            data: A Tick adatokat tartalmazó DataFrame
            date: A dátum, ami alapján a particionálás történik

        Raises:
            ValueError: Ha a DataFrame üres vagy nem tartalmazza a szükséges oszlopokat

        Example:
            >>> import polars as pl
            >>> from datetime import datetime
            >>>
            >>> data = pl.DataFrame({
            ...     'timestamp': [datetime.now()],
            ...     'bid': [1.1000],
            ...     'ask': [1.1002],
            ...     'volume': [1000],
            ...     'source': ['jforex']
            ... })
            >>>
            >>> service = ParquetStorageService()
            >>> await service.store_tick_data('EURUSD', data, datetime.now())

### `read_tick_data`

Tick adatok olvasása dátumtartományból.

        Args:
            symbol: A pénzpár szimbóluma
            start_date: A kezdő dátum
            end_date: A záró dátum

        Returns:
            A Tick adatokat tartalmazó DataFrame

        Example:
            >>> from datetime import datetime, timedelta
            >>>
            >>> service = ParquetStorageService()
            >>> start = datetime(2023, 12, 1)
            >>> end = datetime(2023, 12, 31)
            >>>
            >>> data = await service.read_tick_data('EURUSD', start, end)
            >>> print(f"Loaded {len(data)} ticks")

### `_read_parquet_async`

Aszinkron Parquet olvasás.

        Args:
            path: A Parquet fájl elérési útja

        Returns:
            A beolvasott DataFrame

### `_concat_dataframes`

DataFrame-ek összefűzése a backend típusának megfelelően.

        Args:
            dfs: Az összefűzendő DataFrame-ek listája

        Returns:
            Az összefűzött DataFrame

### `_filter_by_timestamp`

DataFrame szűrése időbélyeg alapján.

        Args:
            data: A szűrendő DataFrame
            start_date: A kezdő dátum
            end_date: A záró dátum

        Returns:
            A szűrt DataFrame

### `get_available_dates`

Elérhető dátumok lekérdezése egy adott szimbólumhoz.

        Args:
            symbol: A pénzpár szimbóluma

        Returns:
            Az elérhető dátumok listája

        Example:
            >>> service = ParquetStorageService()
            >>> dates = await service.get_available_dates('EURUSD')
            >>> print(f"Available dates: {len(dates)}")

### `calculate_checksum`

Adatok checksum számítása integritás ellenőrzéshez.

        Args:
            symbol: A pénzpár szimbóluma
            date: A dátum

        Returns:
            A checksum SHA256 hash

        Example:
            >>> service = ParquetStorageService()
            >>> checksum = await service.calculate_checksum('EURUSD', datetime.now())
            >>> print(f"Checksum: {checksum}")

### `verify_data_integrity`

Adatintegritás ellenőrzése.

        Args:
            symbol: A pénzpár szimbóluma
            date: A dátum

        Returns:
            True ha az adatok integritása megfelelő, egyébként False

        Example:
            >>> service = ParquetStorageService()
            >>> is_valid = await service.verify_data_integrity('EURUSD', datetime.now())
            >>> print(f"Data integrity: {is_valid}")

### `get_storage_stats`

Tárolási statisztikák lekérdezése.

        Args:
            symbol: Opcionális szimbólum szűréshez

        Returns:
            A statisztikákat tartalmazó dictionary

        Example:
            >>> service = ParquetStorageService()
            >>> stats = await service.get_storage_stats('EURUSD')
            >>> print(f"Total files: {stats['total_files']}")

### `save_dataframe`

DataFrame mentése a megadott útvonalra.

        Ez egy adapter metódus a StorageInterface kompatibilitás érdekében.
        A ParquetStorageService saját store_tick_data metódusát használja.

### `load_dataframe`

DataFrame betöltése a megadott útvonalról.

        Ez egy adapter metódus a StorageInterface kompatibilitás érdekében.

### `save_object`

Objektum mentése a megadott útvonalra.

        Ez egy adapter metódus a StorageInterface kompatibilitás érdekében.

### `load_object`

Objektum betöltése a megadott útvonalról.

        Ez egy adapter metódus a StorageInterface kompatibilitás érdekében.

### `exists`

Ellenőrzi, hogy az útvonal létezik-e.

### `get_metadata`

Fájl vagy könyvtár metaadatainak lekérdezése.

### `delete`

Fájl vagy könyvtár törlése.

### `list_dir`

Könyvtár tartalmának listázása.

### `_get_full_path`

Segédfüggvény az útvonal feloldásához.


---

**Forrásfájl:** [`core/storage/implementations/parquet_storage.py`](../../../neural_ai/core/storage/implementations/parquet_storage.py)
