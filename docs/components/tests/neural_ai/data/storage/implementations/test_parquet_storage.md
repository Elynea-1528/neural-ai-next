# 🧪 Teszt: tests/neural_ai/data/storage/implementations/test_parquet_storage.py

**Tesztelt modul:** [`neural_ai/data/storage/implementations/parquet_storage.py`](../../neural_ai/data/storage/implementations/parquet_storage.py)

ParquetStorageService tesztesetek - teljes lefedettséget biztosít.

Ez a modul tartalmazza a ParquetStorageService osztály minden metódusának
egységtesztjeit, biztosítva a 100% kódlefedettséget.

Author: Neural AI Next Team
Version: 2.0.0

## Teszt Osztály: `TestParquetStorageService`

ParquetStorageService osztály tesztesetek.

### ✓ `test_initialization_with_hardware_and_logger()`

Teszteli az inicializációt hardware és logger interfészekkel.

### ✓ `test_initialization_without_hardware_and_logger()`

Teszteli az inicializációt factory-k használatával.

### ✓ `test_backend_selection_avx2()`

Teszteli a PolarsBackend kiválasztását AVX2 támogatással.

### ✓ `test_backend_selection_no_avx2()`

Teszteli a PandasBackend kiválasztását AVX2 nélkül.

### ✓ `test_get_path_with_unique_id()`

Teszteli az elérési út generálást egyedi azonosítóval.

### ✓ `test_get_path_without_unique_id()`

Teszteli az elérési út generálást időbélyeggel.

### ✓ `test_store_tick_data_success()`

Teszteli a tick adatok sikeres tárolását.

### ✓ `test_store_tick_data_empty_dataframe()`

Teszteli az üres DataFrame visszautasítását.

### ✓ `test_store_tick_data_missing_columns()`

Teszteli a hiányzó oszlopok visszautasítását.

### ✓ `test_read_tick_data_no_files()`

Teszteli az olvasást amikor nincsenek fájlok.

### ✓ `test_read_tick_data_with_files()`

Teszteli az olvasást létező fájlokkal.

### ✓ `test_get_available_dates()`

Teszteli az elérhető dátumok lekérdezést.

### ✓ `test_get_available_dates_no_symbol()`

Teszteli az elérhető dátumokat nem létező szimbólum esetén.

### ✓ `test_calculate_checksum_no_files()`

Teszteli a checksum számítást amikor nincsenek fájlok.

### ✓ `test_calculate_checksum_with_files()`

Teszteli a checksum számítást létező fájlokkal.

### ✓ `test_verify_data_integrity_valid()`

Teszteli az adat integritás ellenőrzést érvényes adatokkal.

### ✓ `test_verify_data_integrity_no_files()`

Teszteli az adat integritás ellenőrzést hiányzó fájlok esetén.

### ✓ `test_verify_data_integrity_missing_columns()`

Teszteli az adat integritás ellenőrzést hiányzó oszlopokkal.

### ✓ `test_get_storage_stats()`

Teszteli a tárolási statisztikák lekérdezést.

### ✓ `test_concat_dataframes_polars()`

Teszteli a DataFrame összefűzést Polars esetén.

### ✓ `test_concat_dataframes_pandas()`

Teszteli a DataFrame összefűzést Pandas esetén.

### ✓ `test_deduplicate_data_polars()`

Teszteli a deduplikációt Polars esetén.

### ✓ `test_deduplicate_data_pandas()`

Teszteli a deduplikációt Pandas esetén.

### ✓ `test_sort_by_timestamp_polars()`

Teszteli a rendezést timestamp szerint Polars esetén.

### ✓ `test_sort_by_timestamp_pandas()`

Teszteli a rendezést timestamp szerint Pandas esetén.

### ✓ `test_filter_by_timestamp()`

Teszteli az időbélyeg szerinti szűrést.

### ✓ `test_read_parquet_async()`

Teszteli az aszinkron Parquet olvasást.

### ✓ `test_save_dataframe()`

Teszteli a DataFrame mentését StorageInterface-en keresztül.

### ✓ `test_load_dataframe()`

Teszteli a DataFrame betöltését StorageInterface-en keresztül.

### ✓ `test_exists()`

Teszteli az útvonal létezésének ellenőrzését.

### ✓ `test_get_metadata()`

Teszteli a fájl metaadatainak lekérdezését.

### ✓ `test_delete_file()`

Teszteli a fájl törlését.

### ✓ `test_delete_directory()`

Teszteli a könyvtár törlését.

### ✓ `test_list_dir()`

Teszteli a könyvtár tartalmának listázását.

---

**Teszt fájl:** [`tests/neural_ai/data/storage/implementations/test_parquet_storage.py`](../../tests/neural_ai/data/storage/implementations/test_parquet_storage.py)

**Tesztelt modul:** [`neural_ai/data/storage/implementations/parquet_storage.py`](../../neural_ai/data/storage/implementations/parquet_storage.py)
