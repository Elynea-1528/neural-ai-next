# tests/neural_ai/core/config/interfaces/test_factory_interface.py

ConfigManagerFactoryInterface tesztelése.

Ez a modul tartalmazza a ConfigManagerFactoryInterface interfész teszteit,
amelyek ellenőrzik a konfigurációkezelő factory interfész metódusainak
helyes definícióját és a megvalósító osztályok konzisztenciáját.

## Importok

```python
from abc import ABC
from typing import TYPE_CHECKING
import pytest
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.config.interfaces.factory_interface import ConfigManagerFactoryInterface
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
```

## Konstansok

- **`method_names`**
: `['register_manager', 'get_manager', 'create_manager']`


- **`method`**
: `getattr(ConfigManagerFactoryInterface, method_name)`


- **`method_names`**
: `[name for name in dir(ConfigManagerFactoryInterface) if not name.startswith('_')]`


- **`expected_order`**
: `['register_manager', 'get_manager', 'create_manager']`


- **`manager`**
: `DummyConfigFactory.get_manager('test.yaml')`


- **`manager1`**
: `DummyConfigFactory.get_manager('test1.yaml')`


- **`manager2`**
: `DummyConfigFactory.get_manager('test2.yaml')`


- **`manager1`**
: `DummyConfigFactory.get_manager('config.yaml')`


- **`manager2`**
: `DummyConfigFactory.get_manager('config.yml')`


- **`manager3`**
: `DummyConfigFactory.get_manager('config.json', manager_type='.json')`


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
def get(self) -> object
```

Érték lekérése a konfigurációból.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `object`

#### `get_section()`

```python
def get_section(self, section: str) -> dict[str, object]
```

Teljes konfigurációs szekció lekérése.

**Paraméterek:**

- **`self`**
- **`section`** (`str`)

**Visszatérési érték:**

- Típus: `dict[str, object]`

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
def validate(self, schema: dict[str, object]) -> tuple[bool, dict[str, str] | None]
```

Konfiguráció validálása séma alapján.

**Paraméterek:**

- **`self`**
- **`schema`** (`dict[str, object]`)

**Visszatérési érték:**

- Típus: `tuple[bool, dict[str, str] | None]`

## Osztály: `DummyConfigFactory(ConfigManagerFactoryInterface)`

Egyszerű konfiguráció factory implementáció teszteléshez.

### Metódusok

#### `register_manager()`

```python
def register_manager(cls, extension: str, manager_class: type['ConfigManagerInterface']) -> None
```

Új konfiguráció kezelő típus regisztrálása.

**Paraméterek:**

- **`cls`**
- **`extension`** (`str`)
- **`manager_class`** (`type['ConfigManagerInterface']`)

**Visszatérési érték:**

- Típus: `None`

#### `get_manager()`

```python
def get_manager(cls, filename: str, manager_type: str | None = None) -> 'ConfigManagerInterface'
```

Megfelelő konfiguráció kezelő létrehozása fájlnév vagy típus alapján.

**Paraméterek:**

- **`cls`**
- **`filename`** (`str`)
- **`manager_type`** (`str | None`) = `None`

**Visszatérési érték:**

- Típus: `'ConfigManagerInterface'`

#### `create_manager()`

```python
def create_manager(cls, manager_type: str) -> 'ConfigManagerInterface'
```

Konfiguráció kezelő létrehozása típus alapján.

**Paraméterek:**

- **`cls`**
- **`manager_type`** (`str`)

**Visszatérési érték:**

- Típus: `'ConfigManagerInterface'`

## Osztály: `_IncompleteConfigFactory(ConfigManagerFactoryInterface)`

## Osztály: `TestConfigManagerFactoryInterface`

ConfigManagerFactoryInterface interfész tesztjei.

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

#### `test_interface_methods_are_classmethods()`

```python
def test_interface_methods_are_classmethods(self) -> None
```

Teszteli, hogy az interfész metódusai classmethod-ok.

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

#### `test_register_manager_method()`

```python
def test_register_manager_method(self) -> None
```

Teszteli a register_manager metódust.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_manager_method()`

```python
def test_get_manager_method(self) -> None
```

Teszteli a get_manager metódust.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_manager_with_type()`

```python
def test_get_manager_with_type(self) -> None
```

Teszteli a get_manager metódust explicit típussal.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_manager_with_invalid_extension()`

```python
def test_get_manager_with_invalid_extension(self) -> None
```

Teszteli a get_manager metódust érvénytelen kiterjesztéssel.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_manager_with_invalid_type()`

```python
def test_get_manager_with_invalid_type(self) -> None
```

Teszteli a get_manager metódust érvénytelen típussal.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_create_manager_method()`

```python
def test_create_manager_method(self) -> None
```

Teszteli a create_manager metódust.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_create_manager_with_kwargs()`

```python
def test_create_manager_with_kwargs(self) -> None
```

Teszteli a create_manager metódust csak kulcsszavas argumentumokkal.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_create_manager_with_invalid_type()`

```python
def test_create_manager_with_invalid_type(self) -> None
```

Teszteli a create_manager metódust érvénytelen típussal.

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

### `test_register_manager_raises_not_implemented_error()`

```python
def test_register_manager_raises_not_implemented_error(self) -> None
```

Teszteli, hogy a register_manager alapértelmezésben NotImplementedError-t dob.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_get_manager_raises_not_implemented_error()`

```python
def test_get_manager_raises_not_implemented_error(self) -> None
```

Teszteli, hogy a get_manager alapértelmezésben NotImplementedError-t dob.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_create_manager_raises_not_implemented_error()`

```python
def test_create_manager_raises_not_implemented_error(self) -> None
```

Teszteli, hogy a create_manager alapértelmezésben NotImplementedError-t dob.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_factory_returns_config_manager_interface()`

```python
def test_factory_returns_config_manager_interface(self) -> None
```

Teszteli, hogy a factory ConfigManagerInterface-t ad vissza.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_factory_creates_separate_instances()`

```python
def test_factory_creates_separate_instances(self) -> None
```

Teszteli, hogy a factory külön példányokat hoz létre.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_factory_supports_multiple_manager_types()`

```python
def test_factory_supports_multiple_manager_types(self) -> None
```

Teszteli, hogy a factory támogat több konfigurációkezelő típust.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/core/config/interfaces/test_factory_interface.py`](../../tests/neural_ai/core/config/interfaces/test_factory_interface.py)
