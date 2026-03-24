# 🧪 Teszt: tests/scripts/test_data_reset.py

**Tesztelt modul:** [`scripts/data_reset.py`](../../scripts/data_reset.py)

Data reset szkript teszt modul.

Ez a modul tartalmazza a data_reset.py szkript tesztjeit.

## Teszt Osztály: `TestDataReset`

Data reset szkript tesztjei.

### ✓ `test_check_directory_exists_true()`

Teszteli a könyvtár létezésének ellenőrzését létező könyvtár esetén.

### ✓ `test_check_directory_exists_false_no_dir()`

Teszteli a könyvtár létezésének ellenőrzését nem létező könyvtár esetén.

### ✓ `test_check_directory_exists_false_file()`

Teszteli a könyvtár létezésének ellenőrzését fájl esetén.

### ✓ `test_remove_tick_data_exists()`

Teszteli a tick adatok törlését létező könyvtár esetén.

### ✓ `test_remove_tick_data_not_exists()`

Teszteli a tick adatok törlését nem létező könyvtár esetén.

### ✓ `test_remove_tick_data_exception()`

Teszteli a tick adatok törlését kivétel esetén.

### ✓ `test_remove_logs_exists_with_files()`

Teszteli a logok törlését létező könyvtár esetén fájlokkal.

### ✓ `test_remove_logs_not_exists()`

Teszteli a logok törlését nem létező könyvtár esetén.

### ✓ `test_remove_logs_exception()`

Teszteli a logok törlését kivétel esetén.

### ✓ `test_create_directories_if_needed()`

Teszteli a szükséges könyvtárak létrehozását.

### ✓ `test_main_success()`

Teszteli a main függvényt sikeres végrehajtás esetén.

### ✓ `test_main_failure_tick_data()`

Teszteli a main függvényt tick adatok törlésének sikertelensége esetén.

### ✓ `test_main_failure_logs()`

Teszteli a main függvényt logok törlésének sikertelensége esetén.

### ✓ `test_main_failure_both()`

Teszteli a main függvényt mindkét törlés sikertelensége esetén.

---

**Teszt fájl:** [`tests/scripts/test_data_reset.py`](../../tests/scripts/test_data_reset.py)

**Tesztelt modul:** [`scripts/data_reset.py`](../../scripts/data_reset.py)
