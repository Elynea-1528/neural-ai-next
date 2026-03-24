# 🧪 Teszt: tests/neural_ai/core/test_pyproject_ui_dependencies.py

**Tesztelt modul:** [`neural_ai/core/pyproject_ui_dependencies.py`](../../neural_ai/core/pyproject_ui_dependencies.py)

Teszt a pyproject.toml UI opcionális függőségeinek ellenőrzéséhez.

Ez a teszt ellenőrzi, hogy az ui opcionális függőségi csoport tartalmazza-e
az összes szükséges csomagot a megfelelő verziókkal.

## Teszt Függvények

### ✓ `test_ui_optional_dependencies_exist()`

Ellenőrzi, hogy az 'ui' opcionális függőségi csoport létezik.

### ✓ `test_ui_dependencies_contain_required_packages()`

Ellenőrzi, hogy az 'ui' csoport tartalmazza-e az összes szükséges csomagot.

### ✓ `test_ui_dependencies_have_correct_versions()`

Ellenőrzi a kritikus csomagok verziókövetelményeit.

### ✓ `test_full_includes_ui()`

Ellenőrzi, hogy a 'full' csoport tartalmazza-e az 'ui' csoportot.

### ✓ `test_ui_dependencies_no_duplicates()`

Ellenőrzi, hogy nincsenek-e duplikátumok az 'ui' csoportban.

### ✓ `test_pyproject_toml_is_valid()`

Ellenőrzi, hogy a pyproject.toml érvényes TOML formátumú.

---

**Teszt fájl:** [`tests/neural_ai/core/test_pyproject_ui_dependencies.py`](../../tests/neural_ai/core/test_pyproject_ui_dependencies.py)

**Tesztelt modul:** [`neural_ai/core/pyproject_ui_dependencies.py`](../../neural_ai/core/pyproject_ui_dependencies.py)
