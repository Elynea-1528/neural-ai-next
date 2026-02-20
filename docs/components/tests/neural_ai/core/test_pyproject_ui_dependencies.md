# tests/neural_ai/core/test_pyproject_ui_dependencies.py

Teszt a pyproject.toml UI opcionális függőségeinek ellenőrzéséhez.

Ez a teszt ellenőrzi, hogy az ui opcionális függőségi csoport tartalmazza-e
az összes szükséges csomagot a megfelelő verziókkal.

## Importok

```python
from pathlib import Path
import toml
import pytest
```

## Konstansok

- **`pyproject_path`**
: `Path(__file__).parent.parent.parent / 'pyproject.toml'`


- **`config`**
: `toml.load(f)`


- **`optional_deps`**
: `config.get('project', {}).get('optional-dependencies', {})`


- **`pyproject_path`**
: `Path(__file__).parent.parent.parent / 'pyproject.toml'`


- **`config`**
: `toml.load(f)`


- **`ui_deps`**
: `config['project']['optional-dependencies']['ui']`


- **`required_packages`**
: `['streamlit>=', 'plotly>=', 'streamlit-aggrid', 'watchdog', 'tensorboard', 'torchinfo']`


- **`pyproject_path`**
: `Path(__file__).parent.parent.parent / 'pyproject.toml'`


- **`config`**
: `toml.load(f)`


- **`ui_deps`**
: `config['project']['optional-dependencies']['ui']`


- **`streamlit_dep`**
: `next((dep for dep in ui_deps if 'streamlit' in dep), None)`


- **`plotly_dep`**
: `next((dep for dep in ui_deps if 'plotly' in dep), None)`


- **`pyproject_path`**
: `Path(__file__).parent.parent.parent / 'pyproject.toml'`


- **`config`**
: `toml.load(f)`


- **`full_deps`**
: `config['project']['optional-dependencies']['full']`


- **`pyproject_path`**
: `Path(__file__).parent.parent.parent / 'pyproject.toml'`


- **`config`**
: `toml.load(f)`


- **`ui_deps`**
: `config['project']['optional-dependencies']['ui']`


- **`name`**
: `dep.split('>=')[0].split('==')[0].split('!=')[0].strip()`


- **`pyproject_path`**
: `Path(__file__).parent.parent.parent / 'pyproject.toml'`


### `test_ui_optional_dependencies_exist()`

```python
def test_ui_optional_dependencies_exist() -> None
```

Ellenőrzi, hogy az 'ui' opcionális függőségi csoport létezik.

**Visszatérési érték:**

- Típus: `None`

**Kivételek:**

- **`AssertionError`**: Ha az 'ui' csoport nem létezik vagy üres.

### `test_ui_dependencies_contain_required_packages()`

```python
def test_ui_dependencies_contain_required_packages() -> None
```

Ellenőrzi, hogy az 'ui' csoport tartalmazza-e az összes szükséges csomagot.

**Visszatérési érték:**

- Típus: `None`

**Kivételek:**

- **`AssertionError`**: Ha bármelyik kötelező csomag hiányzik.

### `test_ui_dependencies_have_correct_versions()`

```python
def test_ui_dependencies_have_correct_versions() -> None
```

Ellenőrzi a kritikus csomagok verziókövetelményeit.

**Visszatérési érték:**

- Típus: `None`

**Kivételek:**

- **`AssertionError`**: Ha a verziókövetelmények nem megfelelőek.

### `test_full_includes_ui()`

```python
def test_full_includes_ui() -> None
```

Ellenőrzi, hogy a 'full' csoport tartalmazza-e az 'ui' csoportot.

**Visszatérési érték:**

- Típus: `None`

**Kivételek:**

- **`AssertionError`**: Ha a 'full' csoport nem tartalmazza az 'ui'-t.

### `test_ui_dependencies_no_duplicates()`

```python
def test_ui_dependencies_no_duplicates() -> None
```

Ellenőrzi, hogy nincsenek-e duplikátumok az 'ui' csoportban.

**Visszatérési érték:**

- Típus: `None`

**Kivételek:**

- **`AssertionError`**: Ha duplikátumokat talál.

### `test_pyproject_toml_is_valid()`

```python
def test_pyproject_toml_is_valid() -> None
```

Ellenőrzi, hogy a pyproject.toml érvényes TOML formátumú.

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/core/test_pyproject_ui_dependencies.py`](../../tests/neural_ai/core/test_pyproject_ui_dependencies.py)
