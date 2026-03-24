# 🧪 Teszt: tests/neural_ai/data/storage/test_storage_factory.py

**Tesztelt modul:** [`neural_ai/data/storage/storage_factory.py`](../../neural_ai/data/storage/storage_factory.py)

StorageFactory teszt modul.

Ez a modul tartalmazza a StorageFactory osztály tesztjeit.

## Teszt Osztály: `MockStorage`

## Teszt Osztály: `InvalidClass`

## Teszt Osztály: `FailingStorage`

## Teszt Osztály: `UnexpectedErrorStorage`

## Teszt Osztály: `TestStorageFactory`

StorageFactory osztály tesztjei.

### ✓ `test_register_storage()`

Teszteli a storage típus regisztrálását.

## Teszt Függvények

### ✓ `test_register_storage_invalid_class()`

Teszteli a nem StorageInterface-t implementáló osztály regisztrálását.

### ✓ `test_get_storage_file_type()`

Teszteli a file storage létrehozását.

### ✓ `test_get_storage_parquet_type()`

Teszteli a parquet storage létrehozását.

### ✓ `test_get_storage_with_kwargs()`

Teszteli a storage létrehozást további paraméterekkel.

### ✓ `test_get_storage_invalid_config()`

Teszteli az érvénytelen konfigurációt (pl. tiltott storage típus).

### ✓ `test_get_storage_invalid_type()`

Teszteli a nem létező storage típus lekérését.

### ✓ `test_get_storage_instantiation_failure()`

Teszteli a storage példányosítási hibát.

### ✓ `test_get_storage_unexpected_error()`

Teszteli a váratlan hibát a storage létrehozásakor.

### ✓ `test_get_storage_default_base_path()`

Teszteli a storage létrehozást alapértelmezett útvonallal.

### ✓ `test_get_storage_with_hardware_none()`

Teszteli a storage létrehozást hardware=None paraméterrel.

### ✓ `test_initial_storage_types()`

Teszteli a kezdeti storage típusokat.

---

**Teszt fájl:** [`tests/neural_ai/data/storage/test_storage_factory.py`](../../tests/neural_ai/data/storage/test_storage_factory.py)

**Tesztelt modul:** [`neural_ai/data/storage/storage_factory.py`](../../neural_ai/data/storage/storage_factory.py)
