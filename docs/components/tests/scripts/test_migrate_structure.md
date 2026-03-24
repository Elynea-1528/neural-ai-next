# 🧪 Teszt: tests/scripts/test_migrate_structure.py

**Tesztelt modul:** [`scripts/migrate_structure.py`](../../scripts/migrate_structure.py)

Migrate structure szkript teszt modul.

Ez a modul tartalmazza a migrate_structure.py szkript tesztjeit.

## Teszt Osztály: `TestMigrateStructure`

Migrate structure szkript tesztjei.

### ✓ `test_migrate_tick_structure_no_base_dir()`

Teszteli a migrációt nem létező alapkönyvtár esetén.

### ✓ `test_migrate_tick_structure_no_symbol_dirs()`

Teszteli a migrációt szimbólum könyvtárak nélkül.

### ✓ `test_migrate_tick_structure_no_tick_dir()`

Teszteli a migrációt tick könyvtár nélküli szimbólum esetén.

### ✓ `test_migrate_tick_structure_empty_tick_dir()`

Teszteli a migrációt üres tick könyvtár esetén.

### ✓ `test_migrate_tick_structure_with_content()`

Teszteli a migrációt tick könyvtár tartalommal.

### ✓ `test_migrate_tick_structure_tick_not_dir()`

Teszteli a migrációt amikor a tick 'útvonal' nem mappa.

### ✓ `test_migrate_tick_structure_rmdir_exception_empty()`

Teszteli a migrációt OSError esetén üres tick mappa törlésekor.

### ✓ `test_migrate_tick_structure_target_exists()`

Teszteli a migrációt amikor a célmappa már létezik.

### ✓ `test_migrate_tick_structure_move_exception()`

Teszteli a migrációt OSError esetén az áthelyezéskor.

### ✓ `test_migrate_tick_structure_rmdir_exception_after_move()`

Teszteli a migrációt OSError esetén tick mappa törlésekor tartalom áthelyezése után.

### ✓ `test_main_success()`

Teszteli a main függvényt sikeres végrehajtás esetén.

### ✓ `test_main_logger_none()`

Teszteli a main függvényt None logger esetén.

### ✓ `test_main_exception()`

Teszteli a main függvényt kivétel esetén.

---

**Teszt fájl:** [`tests/scripts/test_migrate_structure.py`](../../tests/scripts/test_migrate_structure.py)

**Tesztelt modul:** [`scripts/migrate_structure.py`](../../scripts/migrate_structure.py)
