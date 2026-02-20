# tests/neural_ai/core/base/interfaces/test_component_interface.py

Component interfészek tesztelése.

Ez a modul tartalmazza a CoreComponentsInterface és CoreComponentFactoryInterface
interfészek egységtesztjeit, amelyek ellenőrzik az interfész definíciók helyességét.

## Importok

```python
import inspect
from typing import TYPE_CHECKING
from typing import Any
from unittest.mock import Mock
from neural_ai.core.base.interfaces.component_interface import CoreComponentFactoryInterface
from neural_ai.core.base.interfaces.component_interface import CoreComponentsInterface
from neural_ai.core.base.interfaces.container_interface import DIContainerInterface
```

## Konstansok

- **`mock_components`**
: `MockCoreComponents()`


- **`components1`**
: `MockCoreComponentFactory.create_components()`


- **`components2`**
: `MockCoreComponentFactory.create_with_container(Mock())`


- **`components3`**
: `MockCoreComponentFactory.create_minimal()`


- **`_`**
: `mock_components.config`


- **`_`**
: `mock_components.logger`


- **`_`**
: `mock_components.storage`


- **`components`**
: `MockCoreComponentFactory.create_components(config_path='/path/to/config', log_path='/path/to/log', storage_path='/path/to/storage')`


- **`mock_container`**
: `Mock(spec=DIContainerInterface)`


- **`components`**
: `MockCoreComponentFactory.create_with_container(mock_container)`


- **`components`**
: `MockCoreComponentFactory.create_minimal()`


## Osztály: `TestCoreComponentsInterface`

CoreComponentsInterface interfész tesztjei.

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

#### `test_interface_has_required_methods()`

```python
def test_interface_has_required_methods(self) -> None
```

Teszteli, hogy az interfész rendelkezik a szükséges metódusokkal.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_interface_methods_are_abstract()`

```python
def test_interface_methods_are_abstract(self) -> None
```

Teszteli, hogy a metódusok absztraktak-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_interface_has_correct_type_hints()`

```python
def test_interface_has_correct_type_hints(self) -> None
```

Teszteli, hogy az interfész metódusainak megfelelő típushintjei vannak.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_interface_properties_accessible()`

```python
def test_interface_properties_accessible(self) -> None
```

Teszteli, hogy az interfész property-jei elérhetők-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `MockCoreComponents(CoreComponentsInterface)`

Mock implementáció a CoreComponentsInterface-hez.

### Metódusok

#### `__init__()`

```python
def __init__(self) -> None
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `config()`

```python
def config(self) -> Any | None
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `Any | None`

#### `logger()`

```python
def logger(self) -> Any | None
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `Any | None`

#### `storage()`

```python
def storage(self) -> Any | None
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `Any | None`

#### `has_config()`

```python
def has_config(self) -> bool
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `bool`

#### `has_logger()`

```python
def has_logger(self) -> bool
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `bool`

#### `has_storage()`

```python
def has_storage(self) -> bool
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `bool`

#### `validate()`

```python
def validate(self) -> bool
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `bool`

## Osztály: `MockCoreComponentFactory(CoreComponentFactoryInterface)`

Mock implementáció a CoreComponentFactoryInterface-hez.

### Metódusok

#### `create_components()`

```python
def create_components(config_path: str | None = None, log_path: str | None = None, storage_path: str | None = None) -> CoreComponentsInterface
```

**Paraméterek:**

- **`config_path`** (`str | None`) = `None`
- **`log_path`** (`str | None`) = `None`
- **`storage_path`** (`str | None`) = `None`

**Visszatérési érték:**

- Típus: `CoreComponentsInterface`

#### `create_with_container()`

```python
def create_with_container(container: Any) -> CoreComponentsInterface
```

**Paraméterek:**

- **`container`** (`Any`)

**Visszatérési érték:**

- Típus: `CoreComponentsInterface`

#### `create_minimal()`

```python
def create_minimal() -> CoreComponentsInterface
```

**Visszatérési érték:**

- Típus: `CoreComponentsInterface`

## Osztály: `MockCoreComponents(CoreComponentsInterface)`

Mock implementáció a CoreComponentsInterface-hez.

### Metódusok

#### `__init__()`

```python
def __init__(self) -> None
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `config()`

```python
def config(self) -> Any | None
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `Any | None`

#### `logger()`

```python
def logger(self) -> Any | None
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `Any | None`

#### `storage()`

```python
def storage(self) -> Any | None
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `Any | None`

#### `has_config()`

```python
def has_config(self) -> bool
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `bool`

#### `has_logger()`

```python
def has_logger(self) -> bool
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `bool`

#### `has_storage()`

```python
def has_storage(self) -> bool
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `bool`

#### `validate()`

```python
def validate(self) -> bool
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `bool`

## Osztály: `MockCoreComponentFactory(CoreComponentFactoryInterface)`

Mock implementáció a CoreComponentFactoryInterface-hez.

### Metódusok

#### `create_components()`

```python
def create_components(config_path: str | None = None, log_path: str | None = None, storage_path: str | None = None) -> CoreComponentsInterface
```

**Paraméterek:**

- **`config_path`** (`str | None`) = `None`
- **`log_path`** (`str | None`) = `None`
- **`storage_path`** (`str | None`) = `None`

**Visszatérési érték:**

- Típus: `CoreComponentsInterface`

#### `create_with_container()`

```python
def create_with_container(container: Any) -> CoreComponentsInterface
```

**Paraméterek:**

- **`container`** (`Any`)

**Visszatérési érték:**

- Típus: `CoreComponentsInterface`

#### `create_minimal()`

```python
def create_minimal() -> CoreComponentsInterface
```

**Visszatérési érték:**

- Típus: `CoreComponentsInterface`

## Osztály: `MockCoreComponents(CoreComponentsInterface)`

Mock implementáció a CoreComponentsInterface-hez.

### Metódusok

#### `__init__()`

```python
def __init__(self) -> None
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `config()`

```python
def config(self) -> Any | None
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `Any | None`

#### `logger()`

```python
def logger(self) -> Any | None
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `Any | None`

#### `storage()`

```python
def storage(self) -> Any | None
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `Any | None`

#### `has_config()`

```python
def has_config(self) -> bool
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `bool`

#### `has_logger()`

```python
def has_logger(self) -> bool
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `bool`

#### `has_storage()`

```python
def has_storage(self) -> bool
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `bool`

#### `validate()`

```python
def validate(self) -> bool
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `bool`

## Osztály: `MockCoreComponentFactory(CoreComponentFactoryInterface)`

Mock implementáció a CoreComponentFactoryInterface-hez.

### Metódusok

#### `create_components()`

```python
def create_components(config_path: str | None = None, log_path: str | None = None, storage_path: str | None = None) -> CoreComponentsInterface
```

**Paraméterek:**

- **`config_path`** (`str | None`) = `None`
- **`log_path`** (`str | None`) = `None`
- **`storage_path`** (`str | None`) = `None`

**Visszatérési érték:**

- Típus: `CoreComponentsInterface`

#### `create_with_container()`

```python
def create_with_container(container: DIContainerInterface) -> CoreComponentsInterface
```

**Paraméterek:**

- **`container`** (`DIContainerInterface`)

**Visszatérési érték:**

- Típus: `CoreComponentsInterface`

#### `create_minimal()`

```python
def create_minimal() -> CoreComponentsInterface
```

**Visszatérési érték:**

- Típus: `CoreComponentsInterface`

## Osztály: `MockCoreComponents(CoreComponentsInterface)`

Mock implementáció a CoreComponentsInterface-hez.

### Metódusok

#### `__init__()`

```python
def __init__(self) -> None
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `config()`

```python
def config(self) -> Any | None
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `Any | None`

#### `logger()`

```python
def logger(self) -> Any | None
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `Any | None`

#### `storage()`

```python
def storage(self) -> Any | None
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `Any | None`

#### `has_config()`

```python
def has_config(self) -> bool
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `bool`

#### `has_logger()`

```python
def has_logger(self) -> bool
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `bool`

#### `has_storage()`

```python
def has_storage(self) -> bool
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `bool`

#### `validate()`

```python
def validate(self) -> bool
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `bool`

## Osztály: `MockCoreComponentFactory(CoreComponentFactoryInterface)`

Mock implementáció a CoreComponentFactoryInterface-hez.

### Metódusok

#### `create_components()`

```python
def create_components(config_path: str | None = None, log_path: str | None = None, storage_path: str | None = None) -> CoreComponentsInterface
```

**Paraméterek:**

- **`config_path`** (`str | None`) = `None`
- **`log_path`** (`str | None`) = `None`
- **`storage_path`** (`str | None`) = `None`

**Visszatérési érték:**

- Típus: `CoreComponentsInterface`

#### `create_with_container()`

```python
def create_with_container(container: Any) -> CoreComponentsInterface
```

**Paraméterek:**

- **`container`** (`Any`)

**Visszatérési érték:**

- Típus: `CoreComponentsInterface`

#### `create_minimal()`

```python
def create_minimal() -> CoreComponentsInterface
```

**Visszatérési érték:**

- Típus: `CoreComponentsInterface`

## Osztály: `TestCoreComponentFactoryInterface`

CoreComponentFactoryInterface interfész tesztjei.

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

#### `test_interface_has_required_methods()`

```python
def test_interface_has_required_methods(self) -> None
```

Teszteli, hogy az interfész rendelkezik a szükséges metódusokkal.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_interface_methods_are_abstract_and_static()`

```python
def test_interface_methods_are_abstract_and_static(self) -> None
```

Teszteli, hogy a metódusok absztraktak és statikusak-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_interface_has_correct_signatures()`

```python
def test_interface_has_correct_signatures(self) -> None
```

Teszteli, hogy az interfész metódusainak megfelelő aláírása van.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_all_abstract_methods_implemented()`

```python
def test_all_abstract_methods_implemented(self) -> None
```

Teszteli, hogy az összes absztrakt metódus implementálva van-e a mockban.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_factory_create_components_with_parameters()`

```python
def test_factory_create_components_with_parameters(self) -> None
```

Teszteli a create_components metódust paraméterekkel (115. sor).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_factory_create_with_container_parameter()`

```python
def test_factory_create_with_container_parameter(self) -> None
```

Teszteli a create_with_container metódust (128. sor).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_factory_create_minimal_implementation()`

```python
def test_factory_create_minimal_implementation(self) -> None
```

Teszteli a create_minimal metódust (138. sor).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/core/base/interfaces/test_component_interface.py`](../../tests/neural_ai/core/base/interfaces/test_component_interface.py)
