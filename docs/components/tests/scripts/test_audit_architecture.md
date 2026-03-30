# 🧪 Teszt: tests/scripts/test_audit_architecture.py

**Tesztelt modul:** [`scripts/audit_architecture.py`](../../scripts/audit_architecture.py)

Integration tesztek a scripts/audit_architecture.py fájlhoz.

Ez a teszt ellenőrzi az Architecture Audit Script teljes workflow-ját,
beleértve a fájl szkennelést, AST elemzést és jelentés generálást.

## Teszt Osztály: `TestAuditArchitectureIntegration`

Integration tesztek az audit_architecture.py script-hez.

### ✓ `test_audit_architecture_script_exists()`

Teszt: Az audit_architecture.py script létezik. Arrange: Projekt gyökér Act: Ellenőrizzük a script létezését Assert: A script fájl létezik és olvasható

### ✓ `test_audit_architecture_imports()`

Teszt: Az audit_architecture modul importálható. Arrange: Projekt gyökér hozzáadása a sys.path-hoz Act: Importáljuk a modult Assert: Nincs ImportError

### ✓ `test_audit_architecture_has_main_class()`

Teszt: Az audit_architecture modul tartalmazza az ArchitectureAuditor osztályt. Arrange: Import a modul Act: Ellenőrizzük az ArchitectureAuditor osztály létezését Assert: Az osztály létezik és példányosítható

### ✓ `test_audit_architecture_scan_codebase()`

Teszt: Az ArchitectureAuditor.scan_codebase metódus működik. Arrange: ArchitectureAuditor példány Act: Szkenneljük a codebase-t Assert: Python fájlok listája nem üres

### ✓ `test_audit_architecture_file_issue_dataclass()`

Teszt: A FileIssue dataclass megfelelően működik. Arrange: Import a FileIssue osztályt Act: Létrehozunk egy FileIssue példányt Assert: A példány megfelelő attribútumokkal rendelkezik

### ✓ `test_audit_architecture_execution_dry_run()`

Teszt: Az audit_architecture.py script futtatható (dry run). Arrange: Script útvonal Act: Futtatjuk a scriptet subprocess-szel (csak import check) Assert: A script nem dob hibát az importáláskor

### ✓ `test_audit_architecture_ignored_dirs()`

Teszt: Az ArchitectureAuditor figyelmen kívül hagyja a cache könyvtárakat. Arrange: ArchitectureAuditor példány Act: Ellenőrizzük az ignored_dirs attribútumot Assert: A cache könyvtárak szerepelnek az ignored_dirs-ben

---

**Teszt fájl:** [`tests/scripts/test_audit_architecture.py`](../../tests/scripts/test_audit_architecture.py)

**Tesztelt modul:** [`scripts/audit_architecture.py`](../../scripts/audit_architecture.py)
