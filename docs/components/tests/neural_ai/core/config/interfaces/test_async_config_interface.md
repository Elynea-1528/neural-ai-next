# tests/neural_ai/core/config/interfaces/test_async_config_interface.py

AsyncConfigManagerInterface tesztelése.

Ez a modul tartalmazza a AsyncConfigManagerInterface interfész teszteit,
amelyek ellenőrzik az aszinkron konfigurációkezelő interfész metódusainak
helyes definícióját és a megvalósító osztályok konzisztenciáját.

## Importok

```python
from abc import ABC
from typing import Any
import pytest
from neural_ai.core.config.interfaces.async_config_interface import AsyncConfigManagerInterface
from neural_ai.core.config.interfaces.async_config_interface import ConfigListener
```

## Konstansok

- **`method_names`**
: `['__init__', 'get', 'get_section', 'set', 'save', 'load', 'load_directory', 'validate', 'add_listener', 'remove_listener', 'start_hot_reload', 'stop_hot_reload', 'get_all', 'set_with_metadata', 'delete']`


- **`method`**
: `getattr(AsyncConfigManagerInterface, method_name)`


- **`method_names`**
: `[name for name in dir(AsyncConfigManagerInterface) if not name.startswith('_')]`


- **`expected_order`**
: `['get', 'get_section', 'set', 'save', 'load', 'load_directory', 'validate', 'add_listener', 'remove_listener', 'start_hot_reload', 'stop_hot_reload', 'get_all', 'set_with_metadata', 'delete']`


- **`manager1`**
: `DummyAsyncConfigManager(filename=None, session=None, logger=None)`


- **`manager2`**
: `DummyAsyncConfigManager()`


- **`manager`**
: `DummyAsyncConfigManager()`


- **`result1`**
: `await manager.get('key1')`


- **`result2`**
: `await manager.get('key2', 'key3')`


- **`manager`**
: `DummyAsyncConfigManager()`


- **`result`**
: `await manager.get('nonexistent', default='default_value')`


- **`manager`**
: `DummyAsyncConfigManager()`


- **`result1`**
: `await manager.get('key1')`


- **`result2`**
: `await manager.get('key2', 'key3')`


- **`manager`**
: `DummyAsyncConfigManager()`


- **`result`**
: `await manager.get_section('test_section')`


- **`manager`**
: `DummyAsyncConfigManager()`


- **`manager`**
: `DummyAsyncConfigManager()`


- **`manager`**
: `DummyAsyncConfigManager()`


- **`manager`**
: `DummyAsyncConfigManager()`


- **`manager`**
: `DummyAsyncConfigManager()`


- **`manager`**
: `DummyAsyncConfigManager()`


- **`manager`**
: `DummyAsyncConfigManager()`


- **`result1`**
: `await manager.get_all(category='system')`


- **`result2`**
: `await manager.get_all()`


- **`manager`**
: `DummyAsyncConfigManager()`


- **`manager`**
: `DummyAsyncConfigManager()`


- **`result1`**
: `await manager.delete('test_key')`


- **`result2`**
: `await manager.delete('nonexistent_key')`


## Osztály: `DummyAsyncConfigManager(AsyncConfigManagerInterface)`

Egyszerű aszinkron konfigurációkezelő implementáció teszteléshez.

### Metódusok

#### `__init__()`

```python
def __init__(self, filename: str | None = None, session: Any | None = None, logger: Any | None = None) -> None
```

Inicializálja a dummy aszinkron konfigurációkezelőt.

**Paraméterek:**

- **`self`**
- **`filename`** (`str | None`) = `None`
- **`session`** (`Any | None`) = `None`
- **`logger`** (`Any | None`) = `None`

**Visszatérési érték:**

- Típus: `None`

#### `get()`

```python
async def get(self) -> Any
```

Érték lekérése a konfigurációból.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `Any`

#### `get_section()`

```python
async def get_section(self, section: str) -> dict[str, Any]
```

Teljes konfigurációs szekció lekérése.

**Paraméterek:**

- **`self`**
- **`section`** (`str`)

**Visszatérési érték:**

- Típus: `dict[str, Any]`

#### `set()`

```python
async def set(self) -> None
```

Érték beállítása a konfigurációban.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `save()`

```python
async def save(self, filename: str | None = None) -> None
```

Konfiguráció mentése.

**Paraméterek:**

- **`self`**
- **`filename`** (`str | None`) = `None`

**Visszatérési érték:**

- Típus: `None`

#### `load()`

```python
async def load(self, filename: str) -> None
```

Konfiguráció betöltése.

**Paraméterek:**

- **`self`**
- **`filename`** (`str`)

**Visszatérési érték:**

- Típus: `None`

#### `load_directory()`

```python
async def load_directory(self, path: str) -> None
```

Betölti az összes konfigurációs fájlt egy mappából.

**Paraméterek:**

- **`self`**
- **`path`** (`str`)

**Visszatérési érték:**

- Típus: `None`

#### `validate()`

```python
async def validate(self, schema: dict[str, Any]) -> tuple[bool, dict[str, str] | None]
```

Konfiguráció validálása séma alapján.

**Paraméterek:**

- **`self`**
- **`schema`** (`dict[str, Any]`)

**Visszatérési érték:**

- Típus: `tuple[bool, dict[str, str] | None]`

#### `add_listener()`

```python
def add_listener(self, callback: ConfigListener) -> None
```

Listener hozzáadása konfiguráció változásokhoz.

**Paraméterek:**

- **`self`**
- **`callback`** (`ConfigListener`)

**Visszatérési érték:**

- Típus: `None`

#### `remove_listener()`

```python
def remove_listener(self, callback: ConfigListener) -> None
```

Listener eltávolítása.

**Paraméterek:**

- **`self`**
- **`callback`** (`ConfigListener`)

**Visszatérési érték:**

- Típus: `None`

#### `start_hot_reload()`

```python
async def start_hot_reload(self, interval: float = 5.0) -> None
```

Hot reload indítása.

**Paraméterek:**

- **`self`**
- **`interval`** (`float`) = `5.0`

**Visszatérési érték:**

- Típus: `None`

#### `stop_hot_reload()`

```python
async def stop_hot_reload(self) -> None
```

Hot reload leállítása.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `get_all()`

```python
async def get_all(self, category: str | None = None) -> dict[str, Any]
```

Összes konfiguráció lekérdezése.

**Paraméterek:**

- **`self`**
- **`category`** (`str | None`) = `None`

**Visszatérési érték:**

- Típus: `dict[str, Any]`

#### `set_with_metadata()`

```python
async def set_with_metadata(self, key: str, value: Any, category: str = 'system', description: str | None = None, is_active: bool = True) -> None
```

Konfiguráció beállítása metaadatokkal.

**Paraméterek:**

- **`self`**
- **`key`** (`str`)
- **`value`** (`Any`)
- **`category`** (`str`) = `'system'`
- **`description`** (`str | None`) = `None`
- **`is_active`** (`bool`) = `True`

**Visszatérési érték:**

- Típus: `None`

#### `delete()`

```python
async def delete(self, key: str) -> bool
```

Konfiguráció törlése (soft delete).

**Paraméterek:**

- **`self`**
- **`key`** (`str`)

**Visszatérési érték:**

- Típus: `bool`

## Osztály: `_IncompleteAsyncConfigManager(AsyncConfigManagerInterface)`

## Osztály: `TestAsyncConfigManagerInterface`

AsyncConfigManagerInterface interfész tesztjei.

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

#### `test_config_listener_type_alias()`

```python
def test_config_listener_type_alias(self) -> None
```

Teszteli a ConfigListener típusalias definícióját.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `sample_listener()`

```python
async def sample_listener(key: str, value: Any) -> None
```

**Paraméterek:**

- **`key`** (`str`)
- **`value`** (`Any`)

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

#### `test_async_methods_are_awaitable()`

```python
async def test_async_methods_are_awaitable(self) -> None
```

Teszteli, hogy az aszinkron metódusok await-elhetőek.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_sync_methods_are_callable()`

```python
def test_sync_methods_are_callable(self) -> None
```

Teszteli, hogy a szinkron metódusok hívhatóak.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `dummy_listener()`

```python
async def dummy_listener(key: str, value: Any) -> None
```

**Paraméterek:**

- **`key`** (`str`)
- **`value`** (`Any`)

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

### `test_constructor_accepts_optional_params()`

```python
def test_constructor_accepts_optional_params(self) -> None
```

Teszteli, hogy a konstruktor elfogadja az opcionális paramétereket.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_get_method_accepts_variable_keys()`

```python
async def test_get_method_accepts_variable_keys(self) -> None
```

Teszteli, hogy a get metódus elfogad változó számú kulcsot.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_get_method_returns_default()`

```python
async def test_get_method_returns_default(self) -> None
```

Teszteli, hogy a get metódus visszaadja az alapértelmezett értéket.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_set_method_accepts_variable_keys()`

```python
async def test_set_method_accepts_variable_keys(self) -> None
```

Teszteli, hogy a set metódus elfogad változó számú kulcsot.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_get_section_returns_dict()`

```python
async def test_get_section_returns_dict(self) -> None
```

Teszteli, hogy a get_section metódus dictionary-t ad vissza.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_validate_returns_tuple()`

```python
async def test_validate_returns_tuple(self) -> None
```

Teszteli, hogy a validate metódus tuple-t ad vissza.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_save_accepts_optional_filename()`

```python
async def test_save_accepts_optional_filename(self) -> None
```

Teszteli, hogy a save metódus elfogad opcionális fájlnevet.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_load_accepts_filename()`

```python
async def test_load_accepts_filename(self) -> None
```

Teszteli, hogy a load metódus elfogad fájlnevet.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_load_directory_accepts_path()`

```python
async def test_load_directory_accepts_path(self) -> None
```

Teszteli, hogy a load_directory metódus elfogad elérési utat.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_start_hot_reload_accepts_interval()`

```python
async def test_start_hot_reload_accepts_interval(self) -> None
```

Teszteli, hogy a start_hot_reload metódus elfogad interval paramétert.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_stop_hot_reload_is_callable()`

```python
async def test_stop_hot_reload_is_callable(self) -> None
```

Teszteli, hogy a stop_hot_reload metódus hívható.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_get_all_accepts_optional_category()`

```python
async def test_get_all_accepts_optional_category(self) -> None
```

Teszteli, hogy a get_all metódus elfogad opcionális kategóriát.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_set_with_metadata_accepts_params()`

```python
async def test_set_with_metadata_accepts_params(self) -> None
```

Teszteli, hogy a set_with_metadata metódus elfogadja a paramétereket.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_delete_returns_bool()`

```python
async def test_delete_returns_bool(self) -> None
```

Teszteli, hogy a delete metódus boolean értéket ad vissza.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/core/config/interfaces/test_async_config_interface.py`](../../tests/neural_ai/core/config/interfaces/test_async_config_interface.py)
