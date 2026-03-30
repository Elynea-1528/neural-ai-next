# 🧪 Teszt: tests/scripts/test_audit_data.py

**Tesztelt modul:** [`scripts/audit_data.py`](../../scripts/audit_data.py)

Integration tesztek a scripts/audit_data.py fájlhoz.

Ez a teszt ellenőrzi az Adatintegritási Audit Script teljes workflow-ját,
beleértve a .bi5 fájlok feldolgozását és a Parquet összehasonlítást.

## Teszt Osztály: `TestAuditDataIntegration`

Integration tesztek az audit_data.py script-hez.

### ✓ `test_audit_data_script_exists()`

Teszt: Az audit_data.py script létezik. Arrange: Projekt gyökér Act: Ellenőrizzük a script létezését Assert: A script fájl létezik és olvasható

### ✓ `test_audit_data_imports()`

Teszt: Az audit_data modul importálható. Arrange: Projekt gyökér hozzáadása a sys.path-hoz Act: Importáljuk a modult Assert: Nincs ImportError

### ✓ `test_audit_data_has_parse_bi5_function()`

Teszt: Az audit_data modul tartalmazza a parse_bi5_file függvényt. Arrange: Import a modul Act: Ellenőrizzük a parse_bi5_file függvény létezését Assert: A függvény létezik és callable

### ✓ `test_audit_data_parse_bi5_with_nonexistent_file()`

Teszt: A parse_bi5_file kezeli a nem létező fájlt. Arrange: Nem létező fájl útvonal Act: Meghívjuk a parse_bi5_file függvényt Assert: Üres lista vagy exception

### ✓ `test_audit_data_execution_dry_run()`

Teszt: Az audit_data.py script futtatható (dry run). Arrange: Script útvonal Act: Futtatjuk a scriptet subprocess-szel (csak import check) Assert: A script nem dob hibát az importáláskor

### ✓ `test_audit_data_has_shebang()`

Teszt: Az audit_data.py script rendelkezik shebang-gel. Arrange: Script útvonal Act: Olvassuk be az első sort Assert: Az első sor shebang

### ✓ `test_audit_data_has_docstring()`

Teszt: Az audit_data modul rendelkezik docstring-gel. Arrange: Import a modul Act: Ellenőrizzük a __doc__ attribútumot Assert: A __doc__ nem None és tartalmazza a leírást

---

**Teszt fájl:** [`tests/scripts/test_audit_data.py`](../../tests/scripts/test_audit_data.py)

**Tesztelt modul:** [`scripts/audit_data.py`](../../scripts/audit_data.py)
