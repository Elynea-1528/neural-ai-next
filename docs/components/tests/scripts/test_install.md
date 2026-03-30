# 🧪 Teszt: tests/scripts/test_install.py

**Tesztelt modul:** [`scripts/install.py`](../../scripts/install.py)

Integration tesztek a scripts/install.py fájlhoz.

Ez a teszt ellenőrzi az Install Script teljes workflow-ját.

## Teszt Osztály: `TestInstallIntegration`

Integration tesztek az install.py script-hez.

### ✓ `test_install_script_exists()`

Teszt: Az install.py script létezik. Arrange: Projekt gyökér Act: Ellenőrizzük a script létezését Assert: A script fájl létezik és olvasható

### ✓ `test_install_imports()`

Teszt: Az install modul importálható. Arrange: Projekt gyökér hozzáadása a sys.path-hoz Act: Importáljuk a modult Assert: Nincs ImportError

### ✓ `test_install_execution_dry_run()`

Teszt: Az install.py script futtatható (dry run). Arrange: Script útvonal Act: Futtatjuk a scriptet subprocess-szel (csak import check) Assert: A script nem dob hibát az importáláskor

### ✓ `test_install_has_shebang()`

Teszt: Az install.py script rendelkezik shebang-gel. Arrange: Script útvonal Act: Olvassuk be az első sort Assert: Az első sor shebang

### ✓ `test_install_has_docstring()`

Teszt: Az install modul rendelkezik docstring-gel. Arrange: Import a modul Act: Ellenőrizzük a __doc__ attribútumot Assert: A __doc__ nem None és tartalmazza a leírást

---

**Teszt fájl:** [`tests/scripts/test_install.py`](../../tests/scripts/test_install.py)

**Tesztelt modul:** [`scripts/install.py`](../../scripts/install.py)
