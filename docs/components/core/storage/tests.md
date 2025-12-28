# Storage Modul Tesztelés

## Áttekintés

A Storage modul átfogó tesztelésen esik át, amely biztosítja a komponensek megbízhatóságát és a várt működést. A tesztek a pytest keretrendszerrel készültek, és 100% code coverage-t céloznak meg.

## Teszt struktúra

A tesztek a következő szerkezetet követik:

```
tests/core/storage/
├── test_factory.py                    # StorageFactory tesztjei
├── backends/
│   ├── test_pandas_backend.py        # PandasBackend tesztjei
│   └── test_polars_backend.py        # PolarsBackend tesztjei
└── implementations/
    ├── test_file_storage.py          # FileStorage tesztjei
    └── test_parquet_storage.py       # ParquetStorageService tesztjei
```

## Tesztesetek

### StorageFactory tesztelés

**Fájl**: [`tests/core/storage/test_factory.py`](../../../tests/core/storage/test_factory.py)

**Tesztosztály**: `TestStorageFactory`

**Tesztesetek:**

1. **`test_register_storage()`**
   - Storage típus regisztrálásának tesztelése
   - Ellenőrzi a sikeres regisztrációt

2. **`test_register_storage_invalid_class()`**
   - Nem StorageInterface-t implementáló osztály regisztrálásának tesztelése

3. **`test_get_storage_file_type()`**
   - File storage létrehozásának tesztelése

4. **`test_get_storage_parquet_type()`**
   - Parquet storage létrehozásának tesztelése hardware detektálással

5. **`test_get_storage_with_kwargs()`**
   - Storage létrehozás további paraméterekkel

6. **`test_get_storage_invalid_type()`**
   - Nem létező storage típus lekérésének tesztelése

7. **`test_get_storage_instantiation_failure()`**
   - Storage példányosítási hiba kezelésének tesztelése

8. **`test_get_storage_unexpected_error()`**
   - Váratlan hibák kezelésének tesztelése

9. **`test_get_storage_default_base_path()`**
   - Alapértelmezett útvonal beállításának tesztelése

10. **`test_get_storage_with_hardware_none()`**
    - Hardware=None paraméter kezelésének tesztelése

11. **`test_initial_storage_types()`**
    - Kezdeti storage típusok ellenőrzése

### FileStorage tesztelés

**Fájl**: [`tests/core/storage/implementations/test_file_storage.py`](../../../tests/core/storage/implementations/test_file_storage.py)

**Tesztosztály**: `TestFileStorage`

**Tesztesetek:**

#### Inicializálás
- `test_init_default_path()`: Alapértelmezett útvonal tesztelése
- `test_init_custom_path()`: Egyéni útvonal tesztelése
- `test_init_with_logger()`: Logger beállítás tesztelése

#### Alapműveletek
- `test_get_full_path_absolute()`: Abszolút útvonal kezelés
- `test_get_full_path_relative()`: Relatív útvonal kezelés
- `test_exists_true()`: Létező fájl ellenőrzés
- `test_exists_false()`: Nem létező fájl ellenőrzés

#### DataFrame műveletek
- `test_save_dataframe_csv()`: DataFrame mentés CSV formátumban
- `test_save_dataframe_excel()`: DataFrame mentés Excel formátumban
- `test_save_dataframe_invalid_format()`: Érvénytelen formátum kezelése
- `test_load_dataframe_not_found()`: Nem létező fájl betöltése

#### Objektum műveletek
- `test_save_object_json()`: Python objektum mentés JSON-ban
- `test_save_object_invalid_format()`: Érvénytelen objektum formátum
- `test_load_object_not_found()`: Nem létező objektum betöltése
- `test_load_object_invalid_json()`: Érvénytelen JSON kezelése

#### Fájlműveletek
- `test_get_metadata_file()`: Fájl metaadatainak lekérdezése
- `test_get_metadata_not_found()`: Nem létező fájl metaadatai
- `test_delete_file()`: Fájl törlése
- `test_delete_not_found()`: Nem létező fájl törlése
- `test_list_dir()`: Könyvtár listázás
- `test_list_dir_with_pattern()`: Könyvtár listázás mintával
- `test_list_dir_not_found()`: Nem létező könyvtár listázása

#### Biztonsági tesztek
- `test_check_permissions_read_only()`: Olvasási jogosultság ellenőrzés
- `test_get_storage_info()`: Tároló információk lekérdezése

#### Belső működés
- `test_atomic_write_json()`: Atomi írás JSON formátumban
- `test_atomic_write_dataframe()`: Atomi írás DataFrame-mel
- `test_setup_format_handlers()`: Formátum kezelők beállítása

### PolarsBackend tesztelés

**Fájl**: [`tests/core/storage/backends/test_polars_backend.py`](../../../tests/core/storage/backends/test_polars_backend.py)

**Tesztosztályok**: `TestPolarsDataFrame`, `TestPolarsBackend`

**Tesztesetek:**

#### PolarsDataFrame wrapper
- `test_init()`: Wrapper inicializálás
- `test_import_polars()`: Lazy import funkcionalitás
- `test_pl_property()`: Polars modul lekérdezés
- `test_pa_property()`: PyArrow modul lekérdezés
- `test_pq_property()`: Parquet modul lekérdezés

#### Backend alapműveletek
- `test_init()`: Backend inicializálás
- `test_ensure_initialized()`: Inicializálás ellenőrzés

#### Írási műveletek
- `test_write_basic()`: Alap írási művelet
- `test_write_with_compression()`: Írás tömörítéssel
- `test_write_invalid_data()`: Érvénytelen adatok kezelése
- `test_write_invalid_path()`: Érvénytelen útvonal kezelése
- `test_write_partitioned()`: Particionált írás

#### Olvasási műveletek
- `test_read_basic()`: Alap olvasási művelet
- `test_read_with_columns()`: Oszlopszűréssel történő olvasás
- `test_read_file_not_found()`: Nem létező fájl olvasása
- `test_read_chunked()`: Chunkolt olvasás
- `test_read_with_filters()`: Szűrőkkel történő olvasás

#### Hozzáfűzési műveletek
- `test_append_to_new_file()`: Hozzáfűzés új fájlhoz
- `test_append_to_existing_file()`: Hozzáfűzés meglévő fájlhoz
- `test_append_with_schema_validation_valid()`: Sémavizsgálat érvényes eset
- `test_append_with_schema_validation_invalid()`: Sémavizsgálat érvénytelen eset
- `test_append_invalid_data()`: Érvénytelen adatok hozzáfűzése

#### Információ lekérdezés
- `test_get_info()`: Fájlinformációk lekérdezése
- `test_get_info_file_not_found()`: Nem létező fájl információi
- `test_supports_format()`: Formátum támogatás ellenőrzése
- `test_validate_data()`: Adatérvényesítés

#### Sémavizsgálat
- `test_validate_schema_valid()`: Érvényes séma ellenőrzése
- `test_validate_schema_invalid()`: Érvénytelen séma ellenőrzése
- `test_validate_schema_exception()`: Kivételkezelés séma ellenőrzésnél

#### Speciális tesztek
- `test_repr()`: String reprezentáció tesztelése
- `test_read_chunked_implementation()`: Chunkolás implementáció tesztelése

### PandasBackend tesztelés

**Fájl**: [`tests/core/storage/backends/test_pandas_backend.py`](../../../tests/core/storage/backends/test_pandas_backend.py)

**Tesztosztályok**: `TestPandasDataFrame`, `TestPandasBackend`

Hasonló teszteseteket tartalmaz mint a PolarsBackend, a Pandas specifikus funkcionalitásokra fókuszálva.

### ParquetStorageService tesztelés

**Fájl**: [`tests/core/storage/implementations/test_parquet_storage.py`](../../../tests/core/storage/implementations/test_parquet_storage.py)

**Tesztosztály**: `TestParquetStorageService`

Komplex integrációs teszteket tartalmaz a teljes Parquet storage pipeline tesztelésére.

## Teszt futtatása

### Összes storage teszt futtatása

```bash
pytest tests/core/storage/ -v
```

### Konkrét tesztfájl futtatása

```bash
pytest tests/core/storage/test_factory.py -v
```

### Konkrét tesztosztály futtatása

```bash
pytest tests/core/storage/implementations/test_file_storage.py::TestFileStorage -v
```

### Coverage jelentés generálása

```bash
pytest tests/core/storage/ --cov=neural_ai.core.storage --cov-report=html
```

## Teszt adatok

A tesztek különböző mintákat használnak:

### DataFrame minták

```python
# Pandas DataFrame
pd.DataFrame({
    'id': [1, 2, 3],
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35]
})

# Polars DataFrame
pl.DataFrame({
    'id': [1, 2, 3],
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35]
})
```

### Objektum minták

```python
{
    'key': 'value',
    'number': 42,
    'nested': {'inner': 'data'}
}
```

### Tick adatok

```python
# Pandas tick data
pd.DataFrame({
    "timestamp": [datetime(2023, 12, 23, 10, 0, 0), ...],
    "bid": [1.1000, 1.1001, 1.1002],
    "ask": [1.1002, 1.1003, 1.1004],
    "volume": [1000, 1200, 1100],
    "source": ["jforex", "jforex", "jforex"],
})

# Polars tick data
pl.DataFrame({
    "timestamp": [datetime(2023, 12, 23, 10, 0, 0), ...],
    "bid": [1.1000, 1.1001, 1.1002],
    "ask": [1.1002, 1.1003, 1.1004],
    "volume": [1000, 1200, 1100],
    "source": ["jforex", "jforex", "jforex"],
})
```

## Mock objektumok

A tesztek mock objektumokat használnak a függőségek helyettesítésére:

### HardwareInterface mock

```python
mock_hardware = MagicMock()
mock_hardware.has_avx2.return_value = True  # vagy False
```

### LoggerInterface mock

```python
mock_logger = MagicMock()
```

## Tesztelési stratégiák

### 1. Unit tesztek

- Egyedi metódusok és osztályok tesztelése
- Független működés ellenőrzése
- Hibakezelés tesztelése

### 2. Integrációs tesztek

- Komponensek együttműködésének tesztelése
- Teljes workflow-ok ellenőrzése
- Valós használati esetek szimulálása

### 3. Túlélési tesztek

- Hibás bemenetek kezelése
- Szélsőséges esetek tesztelése
- Erőforrás korlátok kezelése

### 4. Teljesítmény tesztek

- Nagy adatmennyiségek feldolgozása
- Chunkolás és streaming tesztelése
- Memóriahasználat ellenőrzése

## Best practices

### 1. Tesztelési minta

```python
def test_method_name(self) -> None:
    """Rövid leírás a teszt céljáról."""
    # Arrange - Teszt adatok előkészítése
    test_data = create_test_data()
    
    # Act - Tesztelt művelet végrehajtása
    result = test_method(test_data)
    
    # Assert - Eredmény ellenőrzése
    assert result == expected_result
```

### 2. Fixture használat

```python
@pytest.fixture
def storage(self, temp_dir: Path) -> FileStorage:
    """FileStorage példány létrehozása."""
    return FileStorage(base_path=str(temp_dir))
```

### 3. Paraméterezett tesztek

```python
@pytest.mark.parametrize("input,expected", [
    ("input1", "expected1"),
    ("input2", "expected2"),
])
def test_method(self, input, expected):
    result = process(input)
    assert result == expected
```

### 4. Async tesztelés

```python
@pytest.mark.asyncio
async def test_async_method(self):
    result = await async_method()
    assert result == expected
```

## Hibakeresés

### Teszt futtatás debug módban

```bash
pytest tests/core/storage/ -v --pdb
```

### Konkrét teszt debugolása

```bash
pytest tests/core/storage/test_factory.py::TestStorageFactory::test_get_storage_file_type -v -s
```

### Coverage jelentés

```bash
pytest tests/core/storage/ --cov=neural_ai.core.storage --cov-report=term-missing
```

## Folyamatos integráció

A tesztek a CI/CD folyamat részeként futnak:

1. **Pre-commit hook**: Automatikus teszt futtatás commit előtt
2. **CI pipeline**: Teljes teszt suite futtatása
3. **Coverage ellenőrzés**: Minimum 80% coverage követelmény
4. **Code quality**: Linter ellenőrzések

## Jövőbeli fejlesztések

### Tervezett tesztek

- [ ] Teljesítmény benchmark tesztek
- [ ] Többszálú tesztelés
- [ ] Hálózati hibák szimulálása
- [ ] Memória szivárgás detektálás
- [ ] Stressz tesztek nagy adatmennyiségekre