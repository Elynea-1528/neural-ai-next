# 🧪 Teszt: tests/scripts/test_generate.py

**Tesztelt modul:** [`scripts/generate.py`](../../scripts/generate.py)

Integration tesztek a scripts/generate.py fájlhoz.

Ez a teszt ellenőrzi a Generate Script teljes workflow-ját.

## Teszt Osztály: `TestGenerateIntegration`

Integration tesztek a generate.py script-hez.

### ✓ `test_generate_script_exists()`

Teszt: A generate.py script létezik. Arrange: Projekt gyökér Act: Ellenőrizzük a script létezését Assert: A script fájl létezik és olvasható

### ✓ `test_generate_imports()`

Teszt: A generate modul importálható. Arrange: Projekt gyökér hozzáadása a sys.path-hoz Act: Importáljuk a modult Assert: Nincs ImportError

### ✓ `test_generate_execution_dry_run()`

Teszt: A generate.py script futtatható (dry run). Arrange: Script útvonal Act: Futtatjuk a scriptet subprocess-szel (csak import check) Assert: A script nem dob hibát az importáláskor

### ✓ `test_generate_is_python_file()`

Teszt: A generate.py script Python fájl. Arrange: Script útvonal Act: Ellenőrizzük a fájl kiterjesztését Assert: A fájl .py kiterjesztésű

### ✓ `test_generate_has_docstring()`

Teszt: A generate modul rendelkezik docstring-gel. Arrange: Import a modul Act: Ellenőrizzük a __doc__ attribútumot Assert: A __doc__ nem None és tartalmazza a leírást

---

**Teszt fájl:** [`tests/scripts/test_generate.py`](../../tests/scripts/test_generate.py)

**Tesztelt modul:** [`scripts/generate.py`](../../scripts/generate.py)
