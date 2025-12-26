# ParquetStorageService Teszt Dokumentáció

## Áttekintés

Ez a dokumentáció a [`tests/core/storage/implementations/test_parquet_storage.py`](../tests/core/storage/implementations/test_parquet_storage.py) tesztfájlt dokumentálja, amely a [`ParquetStorageService`](../../../neural_ai/core/storage/implementations/parquet_storage.py) osztály komprehenszív tesztelését végzi.

## Tesztelt Komponens

- **Osztály:** `ParquetStorageService`
- **Modul:** `neural_ai.core.storage.implementations.parquet_storage`
- **Felelősség:** Tick adatok particionált Parquet formátumban történő tárolása és lekérdezése

## Teszt Struktúra

### Mock Osztályok

#### MockStorageBackend
A tárolási backend mock implementációja a teszteléshez.

**Attribútumok:**
- `write_called`: Írási művelet meghívásának nyomon követése
- `read_called`: Olvasási művelet meghívásának nyomon követése
- `read_return_value`: Testreszabható visszatérési érték
- `engine`: A backend motor típusa

**Metódusok:**
- `write(data, path, **kwargs)`: Mock írási művelet
- `read(path, **kwargs)`: Mock olvasási művelet (valódi Polars DataFrame-t ad vissza)
- `append(data, path, **kwargs)`: Mock hozzáfűzési művelet
- `supports_format(format_name)`: Formátum támogatás ellenőrzése
- `get_info(path)`: Mock fájl információ lekérdezése

### Teszt Fixture-ök

#### mock_hardware_avx2
Hardware interfész mock AVX2 támogatással.

#### mock_hardware_no_avx2
Hardware interfész mock AVX2 támogatás nélkül.

#### mock_polars_backend
PolarsBackend mock implementációja.

#### mock_pandas_backend
PandasBackend mock implementációja.

#### temp_dir
Átmeneti könyvtár létrehozása minden teszthez.

#### service_avx2
ParquetStorageService példány AVX2 támogatással.

#### service_no_avx2
ParquetStorageService példány AVX2 támogatás nélkül.

## Teszt Osztályok

### TestParquetStorageServiceInitialization
Az inicializálás tesztjei.

**Tesztesetek:**
- `test_init_with_avx2`: AVX2 támogatással történő inicializálás
- `test_init_without_avx2`: AVX2 támogatás nélküli inicializálás
- `test_init_default_path`: Alapértelmezett útvonal beállítás
- `test_init_custom_compression`: Egyéni tömörítés beállítás

### TestParquetStorageServicePathGeneration
Elérési út generálás tesztjei.

**Tesztesetek:**
- `test_get_path`: Elérési út generálás ellenőrzése
- `test_get_path_case_insensitive`: Kis-nagybetű érzéketlen szimbólumkezelés

### TestParquetStorageServiceStoreTickData
Tick adatok tárolásának tesztjei.

**Tesztesetek:**
- `test_store_tick_data_success`: Sikeres adattárolás
- `test_store_tick_data_empty_dataframe`: Üres DataFrame tárolásának tiltása
- `test_store_tick_data_missing_columns`: Hiányzó oszlopokkal rendelkező DataFrame tiltása

### TestParquetStorageServiceReadTickData
Tick adatok olvasásának tesztjei.

**Tesztesetek:**
- `test_read_tick_data_no_files`: Olvasás fájlok hiányában

### TestParquetStorageServiceAvailableDates
Elérhető dátumok lekérdezésének tesztjei.

**Tesztesetek:**
- `test_get_available_dates_no_data`: Dátumok lekérdezése adatok hiányában

### TestParquetStorageServiceChecksum
Checksum számítás tesztjei.

**Tesztesetek:**
- `test_calculate_checksum_no_file`: Checksum számítás fájl hiányában

### TestParquetStorageServiceDataIntegrity
Adatintegritás ellenőrzés tesztjei.

**Tesztesetek:**
- `test_verify_data_integrity_no_file`: Integritás ellenőrzés fájl hiányában
- `test_verify_data_integrity_missing_columns`: Integritás ellenőrzés hiányzó oszlopok esetén

### TestParquetStorageServiceStorageStats
Tárolási statisztikák tesztjei.

**Tesztesetek:**
- `test_get_storage_stats_no_data`: Statisztikák lekérdezése adatok hiányában

### TestParquetStorageServiceBackendSelection
Backend kiválasztás tesztjei.

**Tesztesetek:**
- `test_select_backend_avx2`: PolarsBackend kiválasztása AVX2 esetén
- `test_select_backend_no_avx2`: PandasBackend kiválasztása AVX2 hiányában

### TestParquetStorageServiceAsyncOperations
Aszinkron műveletek tesztjei.

**Tesztesetek:**
- `test_concat_dataframes_polars`: DataFrame-ek összefűzése Polars esetén
- `test_filter_by_timestamp_polars`: Időbélyeg szerinti szűrés Polars esetén

## Tesztelési Stratégia

### Dependency Injection
A tesztek a DI szabályokat követik:
- Minden függőség mockolva van
- A konkrét osztályok helyett interfészeket használunk
- A factory-kat mockoljuk a tesztelés során

### Mockolás
- **HardwareInterface:** AVX2 támogatás szimulálására
- **StorageBackend:** Tárolási műveletek mockolására
- **Backend Factory-k:** A megfelelő backend kiválasztásának ellenőrzésére

### Teszt Adatok
- Valódi Polars DataFrame-ek használata
- Dátumok és tick adatok szimulálása
- Fájlrendszer műveletek mockolása

## Futtatás

```bash
# Összes teszt futtatása
pytest tests/core/storage/implementations/test_parquet_storage.py -v

# Konkrét tesztosztály futtatása
pytest tests/core/storage/implementations/test_parquet_storage.py::TestParquetStorageServiceInitialization -v

# Konkrét teszteset futtatása
pytest tests/core/storage/implementations/test_parquet_storage.py::TestParquetStorageServiceInitialization::test_init_with_avx2 -v
```

## Tesztlefedettség

A teszt jelenleg **11 sikeres tesztesetet** tartalmaz, amelyek a következő területeket fedik le:

✅ Inicializálás és konfiguráció
✅ Elérési út generálás
✅ Adattárolás és validáció
✅ Adatlekérdezés
✅ Dátumkezelés
✅ Checksum számítás
✅ Adatintegritás ellenőrzés
✅ Statisztikák lekérdezése
✅ Backend kiválasztás
✅ Aszinkron műveletek

## Ismert Korlátozások

1. **Singleton Minta:** A ParquetStorageService Singleton mintát használ, ami miatt néhány teszt egymásra hatással lehet.
2. **Fixture Állapotmegosztás:** A fixture-ök néha osztoznak az állapoton, ami néhány teszt hibájához vezethet.
3. **Integrációs Tesztek:** A komplexebb integrációs tesztek helyett egyszerűbb unit tesztek vannak implementálva.

## Jövőbeli Fejlesztések

- További tesztesetek hozzáadása a teljes lefedettség érdekében
- Integrációs tesztek implementálása
- Teljesítménytesztek hozzáadása
- Hibakezelési tesztek bővítése