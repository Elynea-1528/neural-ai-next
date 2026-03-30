# 🧪 Teszt: tests/scripts/test_force_kill.py

**Tesztelt modul:** [`scripts/force_kill.py`](../../scripts/force_kill.py)

Integration tesztek a scripts/force_kill.py fájlhoz.

Ez a teszt ellenőrzi a Force Kill Script teljes workflow-ját.

## Teszt Osztály: `TestForceKillIntegration`

Integration tesztek a force_kill.py script-hez.

### ✓ `test_force_kill_script_exists()`

Teszt: A force_kill.py script létezik. Arrange: Projekt gyökér Act: Ellenőrizzük a script létezését Assert: A script fájl létezik és olvasható

### ✓ `test_force_kill_imports()`

Teszt: A force_kill modul importálható. Arrange: Projekt gyökér hozzáadása a sys.path-hoz Act: Importáljuk a modult Assert: Nincs ImportError

### ✓ `test_force_kill_execution_dry_run()`

Teszt: A force_kill.py script futtatható (dry run). Arrange: Script útvonal Act: Futtatjuk a scriptet subprocess-szel (csak import check) Assert: A script nem dob hibát az importáláskor

### ✓ `test_force_kill_has_shebang()`

Teszt: A force_kill.py script rendelkezik shebang-gel. Arrange: Script útvonal Act: Olvassuk be az első sort Assert: Az első sor shebang

### ✓ `test_force_kill_has_docstring()`

Teszt: A force_kill modul rendelkezik docstring-gel. Arrange: Import a modul Act: Ellenőrizzük a __doc__ attribútumot Assert: A __doc__ nem None és tartalmazza a leírást

---

**Teszt fájl:** [`tests/scripts/test_force_kill.py`](../../tests/scripts/test_force_kill.py)

**Tesztelt modul:** [`scripts/force_kill.py`](../../scripts/force_kill.py)
