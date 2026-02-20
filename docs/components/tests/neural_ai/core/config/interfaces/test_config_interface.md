# tests/neural_ai/core/config/interfaces/test_config_interface.py

ConfigManagerInterface tesztelése.

Ez a modul tartalmazza a ConfigManagerInterface interfész teszteit,
amelyek ellenőrzik az interfész metódusainak helyes definícióját és
a megvalósító osztályok konzisztenciáját.

## Importok

```python
from abc import ABC
from typing import Any
import pytest
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
```

## Konstansok

- **`manager`**
: `DummyConfigManager()`


- **`method_names`**
: `['__init__', 'get', 'get_section', 'set', 'save', 'load', 'load_directory', 'validate']`


- **`method`**
: `getattr(ConfigManagerInterface, method_name)`


- **`method_names`**
: `[name for name in dir(ConfigManagerInterface) if not name.startswith('_')]`


- **`expected_order`**
: `['get', 'get_section', 'set', 'save', 'load', 'load_directory', 'validate']`


## Osztály: `DummyConfigManager(ConfigManagerInterface)`

Egyszerű konfigurációkezelő implementáció teszteléshez.

### Metódusok

#### `__init__()`

```python
def __init__(self, filename: str | None = None) -> None
```

Inicializálja a dummy konfigurációkezelőt.

**Paraméterek:**

- **`self`**
- **`filename`** (`str | None`) = `None`

**Visszatérési érték:**

- Típus: `None`

#### `get()`

```python
def get(self) -> Any
```

Érték lekérése a konfigurációból.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `Any`

#### `get_section()`

```python
def get_section(self, section: str) -> dict[str, Any]
```

Teljes konfigurációs szekció lekérése.

**Paraméterek:**

- **`self`**
- **`section`** (`str`)

**Visszatérési érték:**

- Típus: `dict[str, Any]`

#### `set()`

```python
def set(self) -> None
```

Érték beállítása a konfigurációban.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `save()`

```python
def save(self, filename: str | None = None) -> None
```

Konfiguráció mentése fájlba.

**Paraméterek:**

- **`self`**
- **`filename`** (`str | None`) = `None`

**Visszatérési érték:**

- Típus: `None`

#### `load()`

```python
def load(self, filename: str) -> None
```

Konfiguráció betöltése fájlból.

**Paraméterek:**

- **`self`**
- **`filename`** (`str`)

**Visszatérési érték:**

- Típus: `None`

#### `load_directory()`

```python
def load_directory(self, path: str) -> None
```

Betölti az összes YAML fájlt egy mappából namespaced struktúrába.

**Paraméterek:**

- **`self`**
- **`path`** (`str`)

**Visszatérési érték:**

- Típus: `None`

#### `validate()`

```python
def validate(self, schema: dict[str, Any]) -> tuple[bool, dict[str, str] | None]
```

Konfiguráció validálása séma alapján.

**Paraméterek:**

- **`self`**
- **`schema`** (`dict[str, Any]`)

**Visszatérési érték:**

- Típus: `tuple[bool, dict[str, str] | None]`

## Osztály: `_IncompleteConfigManager(ConfigManagerInterface)`

## Osztály: `TestConfigManagerInterface`

ConfigManagerInterface interfész tesztjei.

### Metódusok

#### `test_interface_is_abstract()`

```python
def test_interface_is_abstract(self) -> None
```

Teszteli, hogy az interfész absztrakt osztály-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_interface_has_abstract_methods()`

```python
def test_interface_has_abstract_methods(self) -> None
```

Teszteli, hogy az interfész tartalmazza a szükséges absztrakt metódusokat.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_interface_method_signatures()`

```python
def test_interface_method_signatures(self) -> None
```

Teszteli a metódusok aláírásainak helyességét.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_implementation_can_be_instantiated()`

```python
def test_implementation_can_be_instantiated(self) -> None
```

Teszteli, hogy az interfész implementálható-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_implementation_has_all_methods()`

```python
def test_implementation_has_all_methods(self) -> None
```

Teszteli, hogy az implementáció tartalmazza az összes szükséges metódust.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_method_accepts_variable_keys()`

```python
def test_get_method_accepts_variable_keys(self) -> None
```

Teszteli, hogy a get metódus elfogad változó számú kulcsot.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_method_returns_default()`

```python
def test_get_method_returns_default(self) -> None
```

Teszteli, hogy a get metódus visszaadja az alapértelmezett értéket.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_set_method_accepts_variable_keys()`

```python
def test_set_method_accepts_variable_keys(self) -> None
```

Teszteli, hogy a set metódus elfogad változó számú kulcsot.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_section_returns_dict()`

```python
def test_get_section_returns_dict(self) -> None
```

Teszteli, hogy a get_section metódus dictionary-t ad vissza.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_validate_returns_tuple()`

```python
def test_validate_returns_tuple(self) -> None
```

Teszteli, hogy a validate metódus tuple-t ad vissza.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_save_accepts_optional_filename()`

```python
def test_save_accepts_optional_filename(self) -> None
```

Teszteli, hogy a save metódus elfogad opcionális fájlnevet.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_load_accepts_filename()`

```python
def test_load_accepts_filename(self) -> None
```

Teszteli, hogy a load metódus elfogad fájlnevet.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_load_directory_accepts_path()`

```python
def test_load_directory_accepts_path(self) -> None
```

Teszteli, hogy a load_directory metódus elfogad elérési utat.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_interface_enforces_method_implementation()`

```python
def test_interface_enforces_method_implementation(self) -> None
```

Teszteli, hogy az interfész kényszeríti a metódusok implementálását.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_implementation_preserves_type_hints()`

```python
def test_implementation_preserves_type_hints(self) -> None
```

Teszteli, hogy az implementáció megőrzi a típusjelzéseket.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_interface_docstrings_present()`

```python
def test_interface_docstrings_present(self) -> None
```

Teszteli, hogy az interfész metódusainak van docstringje.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_interface_method_order()`

```python
def test_interface_method_order(self) -> None
```

Teszteli, hogy az interfész metódusai logikus sorrendben vannak.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/core/config/interfaces/test_config_interface.py`](../../tests/neural_ai/core/config/interfaces/test_config_interface.py)
