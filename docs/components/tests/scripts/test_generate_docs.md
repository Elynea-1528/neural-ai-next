# 🧪 Teszt: tests/scripts/test_generate_docs.py

**Tesztelt modul:** [`scripts/generate_docs.py`](../../scripts/generate_docs.py)

Integration tesztek a scripts/generate_docs.py fájlhoz.

Ez a teszt ellenőrzi a Generate Docs Script teljes workflow-ját.

## Teszt Osztály: `TestGenerateDocsIntegration`

Integration tesztek a generate_docs.py script-hez.

### ✓ `test_generate_docs_script_exists()`

Teszt: A generate_docs.py script létezik. Arrange: Projekt gyökér Act: Ellenőrizzük a script létezését Assert: A script fájl létezik és olvasható

### ✓ `test_generate_docs_imports()`

Teszt: A generate_docs modul importálható. Arrange: Projekt gyökér hozzáadása a sys.path-hoz Act: Importáljuk a modult Assert: Nincs ImportError

### ✓ `test_generate_docs_execution_dry_run()`

Teszt: A generate_docs.py script futtatható (dry run). Arrange: Script útvonal Act: Futtatjuk a scriptet subprocess-szel (csak import check) Assert: A script nem dob hibát az importáláskor

### ✓ `test_generate_docs_has_shebang()`

Teszt: A generate_docs.py script rendelkezik shebang-gel. Arrange: Script útvonal Act: Olvassuk be az első sort Assert: Az első sor shebang

### ✓ `test_generate_docs_has_docstring()`

Teszt: A generate_docs modul rendelkezik docstring-gel. Arrange: Import a modul Act: Ellenőrizzük a __doc__ attribútumot Assert: A __doc__ nem None és tartalmazza a leírást

---

**Teszt fájl:** [`tests/scripts/test_generate_docs.py`](../../tests/scripts/test_generate_docs.py)

**Tesztelt modul:** [`scripts/generate_docs.py`](../../scripts/generate_docs.py)
