# neural_ai/data/storage/implementations/parquet_storage.py

ParquetStorageService - Particionált Parquet tároló szolgáltatás.

Ez az osztály implementálja a Tick adatok particionált Parquet formátumban történő tárolását
és lekérdezését a Neural AI Next rendszer számára. A tárolás dátum és szimbólum alapú
particionálást használ a gyors lekérdezés érdekében.

A szolgáltatás hardver-gyorsítást detektál és automatikusan kiválasztja a legoptimálisabb
backend-et (PolarsBackend AVX2 támogatással, vagy PandasBackend kompatibilitási módban).

## Osztályok

### `ParquetStorageService`

Particionált Parquet tároló szolgáltatás backend selectorral.

Ez az osztály felelős a Tick adatok particionált Parquet formátumban történő
tárolásáért és lekérdezéséért. A particionálás dátum és szimbólum alapú,
ami lehetővé teszi a gyors és hatékony adatlekérdezést.

A szolgáltatás automatikusan detektálja a hardver képességeket és kiválasztja
a legoptimálisabb tárolási backend-et.

Attributes:
    BASE_PATH: A tárolás alapútvonala
    engine: A Parquet engine ('fastparquet' vagy 'polars')
    compression: Tömörítési algoritmus ('snappy')
    backend: A kiválasztott tárolási backend

## Főbb metódusok

- `store_tick_data`: Tick adatok tárolása particionált Parquet formátumban
- `read_tick_data`: Tick adatok olvasása dátumtartományból
- `get_available_dates`: Elérhető dátumok lekérdezése
- `calculate_checksum`: Adatok checksum számítása integritás ellenőrzéshez
- `verify_data_integrity`: Adatintegritás ellenőrzése

---

**Forrásfájl:** [`neural_ai/data/storage/implementations/parquet_storage.py`](../../../neural_ai/data/storage/implementations/parquet_storage.py)