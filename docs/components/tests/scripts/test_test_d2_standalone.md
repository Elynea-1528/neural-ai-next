# 🧪 Teszt: tests/scripts/test_test_d2_standalone.py

**Tesztelt modul:** [`scripts/d2_standalone.py`](../../scripts/d2_standalone.py)

Integration tesztek a scripts/test_d2_standalone.py fájlhoz.

Ez a teszt ellenőrzi a Test D2 Standalone Script teljes workflow-ját.

## Teszt Osztály: `TestD2StandaloneIntegration`

Integration tesztek a test_d2_standalone.py script-hez.

### ✓ `test_d2_standalone_script_exists()`

Teszt: A test_d2_standalone.py script létezik. Arrange: Projekt gyökér Act: Ellenőrizzük a script létezését Assert: A script fájl létezik és olvasható

### ✓ `test_d2_standalone_imports()`

Teszt: A test_d2_standalone modul importálható. Arrange: Projekt gyökér hozzáadása a sys.path-hoz Act: Importáljuk a modult Assert: Nincs ImportError

### ✓ `test_d2_standalone_execution_dry_run()`

Teszt: A test_d2_standalone.py script futtatható (dry run). Arrange: Script útvonal Act: Futtatjuk a scriptet subprocess-szel (csak import check) Assert: A script nem dob hibát az importáláskor

### ✓ `test_d2_standalone_has_shebang()`

Teszt: A test_d2_standalone.py script rendelkezik shebang-gel. Arrange: Script útvonal Act: Olvassuk be az első sort Assert: Az első sor shebang

### ✓ `test_d2_standalone_has_docstring()`

Teszt: A test_d2_standalone modul rendelkezik docstring-gel. Arrange: Import a modul Act: Ellenőrizzük a __doc__ attribútumot Assert: A __doc__ nem None és tartalmazza a leírást

---

**Teszt fájl:** [`tests/scripts/test_test_d2_standalone.py`](../../tests/scripts/test_test_d2_standalone.py)

**Tesztelt modul:** [`scripts/d2_standalone.py`](../../scripts/d2_standalone.py)
