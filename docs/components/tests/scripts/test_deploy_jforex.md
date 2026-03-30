# 🧪 Teszt: tests/scripts/test_deploy_jforex.py

**Tesztelt modul:** [`scripts/deploy_jforex.py`](../../scripts/deploy_jforex.py)

Integration tesztek a scripts/deploy_jforex.py fájlhoz.

Ez a teszt ellenőrzi a JForex Deploy Script teljes workflow-ját.

## Teszt Osztály: `TestDeployJForexIntegration`

Integration tesztek a deploy_jforex.py script-hez.

### ✓ `test_deploy_jforex_script_exists()`

Teszt: A deploy_jforex.py script létezik. Arrange: Projekt gyökér Act: Ellenőrizzük a script létezését Assert: A script fájl létezik és olvasható

### ✓ `test_deploy_jforex_imports()`

Teszt: A deploy_jforex modul importálható. Arrange: Projekt gyökér hozzáadása a sys.path-hoz Act: Importáljuk a modult Assert: Nincs ImportError

### ✓ `test_deploy_jforex_execution_dry_run()`

Teszt: A deploy_jforex.py script futtatható (dry run). Arrange: Script útvonal Act: Futtatjuk a scriptet subprocess-szel (csak import check) Assert: A script nem dob hibát az importáláskor

### ✓ `test_deploy_jforex_has_shebang()`

Teszt: A deploy_jforex.py script rendelkezik shebang-gel. Arrange: Script útvonal Act: Olvassuk be az első sort Assert: Az első sor shebang

### ✓ `test_deploy_jforex_has_docstring()`

Teszt: A deploy_jforex modul rendelkezik docstring-gel. Arrange: Import a modul Act: Ellenőrizzük a __doc__ attribútumot Assert: A __doc__ nem None és tartalmazza a leírást

---

**Teszt fájl:** [`tests/scripts/test_deploy_jforex.py`](../../tests/scripts/test_deploy_jforex.py)

**Tesztelt modul:** [`scripts/deploy_jforex.py`](../../scripts/deploy_jforex.py)
