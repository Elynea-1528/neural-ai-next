# ParquetStorageService Tesztek Dokumentációja

## Áttekintés

Ez a dokumentáció a [`tests/core/storage/implementations/test_parquet_storage.py`](../tests/core/storage/implementations/test_parquet_storage.py) tesztfájlt dokumentálja, amely a [`ParquetStorageService`](../../../neural_ai/core/storage/implementations/parquet_storage.py) osztály funkcionalitását teszteli.

## Tesztosztályok

### 1. TestParquetStorageService

A fő tesztosztály, amely a `ParquetStorageService` alapvető funkcionalitását teszteli.

#### Fontosabb tesztek:

- **Backend kiválasztás tesztelése**:
  - `test_init_with_avx2_support`: Ellenőrzi, hogy AVX2 támogatás esetén a PolarsBackend kerül-e kiválasztásra
  - `test_init_without_avx2_support`: Ellenőrzi, hogy AVX2 hiányában a PandasBackend kerül-e kiválasztásra

- **Adattárolás és olvasás**:
  - `test_store_tick_data_polars`: Teszteli a Polars DataFrame tárolását
  - `test_read_tick_data_polars`: Teszteli a Polars DataFrame olvasását
  - `test_read_tick_data_multiple_days`: Teszteli a több napos adatok olvasását

- **Hibakezelés**:
  - `test_store_empty_dataframe_raises_error`: Ellenőrzi, hogy üres DataFrame tárolása hibát dob-e
  - `test_store_dataframe_missing_columns_raises_error`: Ellenőrzi, hogy hiányzó oszlopok esetén hiba keletkezik-e

- **Adatintegritás**:
  - `test_calculate_checksum`: Teszteli a checksum számítást
  - `test_verify_data_integrity_success`: Teszteli az adatintegritás ellenőrzését sikeres esetben
  - `test_verify_data_integrity_no_file`: Teszteli az adatintegritás ellenőrzését, ha nincs fájl

- **Tárolási statisztikák**:
  - `test_get_storage_stats`: Teszteli a tárolási statisztikák lekérdezését
  - `test_get_storage_stats_with_symbol`: Teszteli a tárolási statisztikák lekérdezését szimbólum szerint

- **Speciális funkcionalitások**:
  - `test_store_multiple_files_same_day`: Teszteli, hogy több fájl is létrejöhet-e egy napon
  - `test_read_with_deduplication`: Teszteli a deduplikációt olvasáskor
  - `test_read_with_sorting`: Teszteli a rendezettséget olvasáskor

### 2. TestParquetStorageAdapterMethods

A második tesztosztály, amely a `StorageInterface` adapter metódusokat teszteli.

#### Fontosabb tesztek:

- **Alapvető adapter metódusok**:
  - `test_adapter_save_object`: Teszteli a `save_object` metódust
  - `test_adapter_load_object`: Teszteli a `load_object` metódust
  - `test_adapter_exists`: Teszteli az `exists` metódust
  - `test_adapter_delete`: Teszteli a `delete` metódust
  - `test_adapter_get_metadata`: Teszteli a `get_metadata` metódust
  - `test_adapter_list_dir`: Teszteli a `list_dir` metódust

- **Hibakezelés**:
  - `test_adapter_load_object_not_found`: Teszteli a `load_object` hibakezelését
  - `test_adapter_delete_not_found`: Teszteli a `delete` hibakezelését
  - `test_adapter_get_metadata_not_found`: Teszteli a `get_metadata` hibakezelését
  - `test_adapter_list_dir_not_found`: Teszteli a `list_dir` hibakezelését
  - `test_adapter_list_dir_on_file`: Teszteli a `list_dir` hibakezelését fájlra

- **Speciális funkcionalitások**:
  - `test_adapter_save_object_with_nested_path`: Teszteli a `save_object`-ot beágyazott útvonallal
  - `test_adapter_exists_for_directory`: Teszteli az `exists` metódust könyvtárra
  - `test_adapter_delete_directory`: Teszteli a `delete` metódust könyvtárra
  - `test_adapter_get_metadata_for_directory`: Teszteli a `get_metadata` metódust könyvtárra
  - `test_adapter_list_dir_with_pattern`: Teszteli a `list_dir` metódust glob patternmel

- **Smart filename generálás**:
  - `test_smart_filename_uniqueness`: Ellenőrzi, hogy egyedi fájlneveket generál-e
  - `test_smart_filename_with_custom_unique_id`: Teszteli az egyedi azonosítóval történő fájlnév generálást
  - `test_smart_filename_path_structure`: Ellenőrzi a helyes útvonalszerkezetet

- **DataFrame adapter metódusok**:
  - `test_adapter_save_dataframe_sync`: Teszteli a `save_dataframe` adapter metódust szinkron hívásra
  - `test_adapter_load_dataframe_sync`: Teszteli a `load_dataframe` adapter metódust szinkron hívásra

## Teszt Coverage

A tesztek jelenleg **83%** coverage-t érnek el a `parquet_storage.py` fájlon. A hiányzó sorok főleg:

- A PandasBackend-hez kapcsolódó ágak (amelyek a `@pytest.mark.skip` annotáció miatt nincsenek tesztelve)
- Néhány hibakezelési ág
- Néhány ritkán használt metódus

## Futtatás

A teszteket a következő paranccsal lehet futtatni:

```bash
# Összes teszt futtatása
pytest tests/core/storage/implementations/test_parquet_storage.py -v

# Coverage jelentéssel
pytest tests/core/storage/implementations/test_parquet_storage.py --cov=neural_ai.core.storage.implementations.parquet_storage --cov-report=term-missing

# Csak az adapter metódusok tesztelése
pytest tests/core/storage/implementations/test_parquet_storage.py::TestParquetStorageAdapterMethods -v
```

## Függőségek

A tesztek a következő külső könyvtárakat használják:

- `pytest`: Tesztkeretrendszer
- `pytest-asyncio`: Aszinkron tesztek támogatása
- `pytest-cov`: Coverage jelentés generálása
- `pandas`: DataFrame kezelés
- `polars`: Gyorsabb DataFrame kezelés
- `tempfile`: Ideiglenes fájlok létrehozása
- `shutil`: Fájlrendszer műveletek
- `unittest.mock`: Mock objektumok létrehozása

## Jegyzetek

- A tesztesetek minden esetben tiszta állapotból indulnak (Singleton cache törlése)
- Az ideiglenes fájlokat a teszt végén automatikusan törli a rendszer
- A mockolt objektumok lehetővé teszik a hardverfüggő részek tesztelését
- A kihagyott tesztek (`@pytest.mark.skip`) kompatibilitási problémák miatt vannak kihagyva