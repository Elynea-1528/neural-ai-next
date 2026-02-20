# tests/neural_ai/core/base/interfaces/test_container_interface.py

Container interfészek tesztelése.

Ez a modul tartalmazza a DIContainerInterface és LazyComponentInterface
interfészek egységtesztjeit, amelyek ellenőrzik az interfész definíciók helyességét.

## Importok

```python
import inspect
from typing import Any
from unittest.mock import Mock
from neural_ai.core.base.interfaces.container_interface import DIContainerInterface
from neural_ai.core.base.interfaces.container_interface import LazyComponentInterface
```

## Konstansok

- **`container`**
: `MockContainer()`


- **`mock_instance`**
: `Mock()`


- **`container`**
: `MockContainer()`


- **`container`**
: `MockContainer()`


- **`mock_instance`**
: `Mock()`


- **`container`**
: `MockContainer()`


- **`container`**
: `MockContainer()`


- **`result`**
: `container.get('test_component')`


- **`container`**
: `MockContainer()`


- **`component`**
: `MockLazyComponent()`


- **`value`**
: `component.get()`


- **`component`**
: `MockLazyComponent()`


## Osztály: `MockContainer(DIContainerInterface)`

Mock implementáció a DIContainerInterface-hez.

### Metódusok

#### `__init__()`

```python
def __init__(self) -> None
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `register_instance()`

```python
def register_instance(self, interface: Any, instance: Any) -> None
```

**Paraméterek:**

- **`self`**
- **`interface`** (`Any`)
- **`instance`** (`Any`)

**Visszatérési érték:**

- Típus: `None`

#### `register_factory()`

```python
def register_factory(self, interface: Any, factory: Any) -> None
```

**Paraméterek:**

- **`self`**
- **`interface`** (`Any`)
- **`factory`** (`Any`)

**Visszatérési érték:**

- Típus: `None`

#### `resolve()`

```python
def resolve(self, interface: Any) -> Any | None
```

**Paraméterek:**

- **`self`**
- **`interface`** (`Any`)

**Visszatérési érték:**

- Típus: `Any | None`

#### `register_lazy()`

```python
def register_lazy(self, component_name: str, factory_func: Any) -> None
```

**Paraméterek:**

- **`self`**
- **`component_name`** (`str`)
- **`factory_func`** (`Any`)

**Visszatérési érték:**

- Típus: `None`

#### `get()`

```python
def get(self, component_name: str) -> object
```

**Paraméterek:**

- **`self`**
- **`component_name`** (`str`)

**Visszatérési érték:**

- Típus: `object`

#### `clear()`

```python
def clear(self) -> None
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `MockContainer(DIContainerInterface)`

Mock implementáció a DIContainerInterface-hez.

### Metódusok

#### `__init__()`

```python
def __init__(self) -> None
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `register_instance()`

```python
def register_instance(self, interface: Any, instance: Any) -> None
```

**Paraméterek:**

- **`self`**
- **`interface`** (`Any`)
- **`instance`** (`Any`)

**Visszatérési érték:**

- Típus: `None`

#### `register_factory()`

```python
def register_factory(self, interface: Any, factory: Any) -> None
```

**Paraméterek:**

- **`self`**
- **`interface`** (`Any`)
- **`factory`** (`Any`)

**Visszatérési érték:**

- Típus: `None`

#### `resolve()`

```python
def resolve(self, interface: Any) -> Any | None
```

**Paraméterek:**

- **`self`**
- **`interface`** (`Any`)

**Visszatérési érték:**

- Típus: `Any | None`

#### `register_lazy()`

```python
def register_lazy(self, component_name: str, factory_func: Any) -> None
```

**Paraméterek:**

- **`self`**
- **`component_name`** (`str`)
- **`factory_func`** (`Any`)

**Visszatérési érték:**

- Típus: `None`

#### `get()`

```python
def get(self, component_name: str) -> object
```

**Paraméterek:**

- **`self`**
- **`component_name`** (`str`)

**Visszatérési érték:**

- Típus: `object`

#### `clear()`

```python
def clear(self) -> None
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `MockContainer(DIContainerInterface)`

Mock implementáció a DIContainerInterface-hez.

### Metódusok

#### `__init__()`

```python
def __init__(self) -> None
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `register_instance()`

```python
def register_instance(self, interface: Any, instance: Any) -> None
```

**Paraméterek:**

- **`self`**
- **`interface`** (`Any`)
- **`instance`** (`Any`)

**Visszatérési érték:**

- Típus: `None`

#### `register_factory()`

```python
def register_factory(self, interface: Any, factory: Any) -> None
```

**Paraméterek:**

- **`self`**
- **`interface`** (`Any`)
- **`factory`** (`Any`)

**Visszatérési érték:**

- Típus: `None`

#### `resolve()`

```python
def resolve(self, interface: Any) -> Any | None
```

**Paraméterek:**

- **`self`**
- **`interface`** (`Any`)

**Visszatérési érték:**

- Típus: `Any | None`

#### `register_lazy()`

```python
def register_lazy(self, component_name: str, factory_func: Any) -> None
```

**Paraméterek:**

- **`self`**
- **`component_name`** (`str`)
- **`factory_func`** (`Any`)

**Visszatérési érték:**

- Típus: `None`

#### `get()`

```python
def get(self, component_name: str) -> object
```

**Paraméterek:**

- **`self`**
- **`component_name`** (`str`)

**Visszatérési érték:**

- Típus: `object`

#### `clear()`

```python
def clear(self) -> None
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `MockContainer(DIContainerInterface)`

Mock implementáció a DIContainerInterface-hez.

### Metódusok

#### `__init__()`

```python
def __init__(self) -> None
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `register_instance()`

```python
def register_instance(self, interface: Any, instance: Any) -> None
```

**Paraméterek:**

- **`self`**
- **`interface`** (`Any`)
- **`instance`** (`Any`)

**Visszatérési érték:**

- Típus: `None`

#### `register_factory()`

```python
def register_factory(self, interface: Any, factory: Any) -> None
```

**Paraméterek:**

- **`self`**
- **`interface`** (`Any`)
- **`factory`** (`Any`)

**Visszatérési érték:**

- Típus: `None`

#### `resolve()`

```python
def resolve(self, interface: Any) -> Any | None
```

**Paraméterek:**

- **`self`**
- **`interface`** (`Any`)

**Visszatérési érték:**

- Típus: `Any | None`

#### `register_lazy()`

```python
def register_lazy(self, component_name: str, factory_func: Any) -> None
```

**Paraméterek:**

- **`self`**
- **`component_name`** (`str`)
- **`factory_func`** (`Any`)

**Visszatérési érték:**

- Típus: `None`

#### `get()`

```python
def get(self, component_name: str) -> object
```

**Paraméterek:**

- **`self`**
- **`component_name`** (`str`)

**Visszatérési érték:**

- Típus: `object`

#### `clear()`

```python
def clear(self) -> None
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `MockContainer(DIContainerInterface)`

Mock implementáció a DIContainerInterface-hez.

### Metódusok

#### `__init__()`

```python
def __init__(self) -> None
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `register_instance()`

```python
def register_instance(self, interface: Any, instance: Any) -> None
```

**Paraméterek:**

- **`self`**
- **`interface`** (`Any`)
- **`instance`** (`Any`)

**Visszatérési érték:**

- Típus: `None`

#### `register_factory()`

```python
def register_factory(self, interface: Any, factory: Any) -> None
```

**Paraméterek:**

- **`self`**
- **`interface`** (`Any`)
- **`factory`** (`Any`)

**Visszatérési érték:**

- Típus: `None`

#### `resolve()`

```python
def resolve(self, interface: Any) -> Any | None
```

**Paraméterek:**

- **`self`**
- **`interface`** (`Any`)

**Visszatérési érték:**

- Típus: `Any | None`

#### `register_lazy()`

```python
def register_lazy(self, component_name: str, factory_func: Any) -> None
```

**Paraméterek:**

- **`self`**
- **`component_name`** (`str`)
- **`factory_func`** (`Any`)

**Visszatérési érték:**

- Típus: `None`

#### `get()`

```python
def get(self, component_name: str) -> object
```

**Paraméterek:**

- **`self`**
- **`component_name`** (`str`)

**Visszatérési érték:**

- Típus: `object`

#### `clear()`

```python
def clear(self) -> None
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `MockContainer(DIContainerInterface)`

Mock implementáció a DIContainerInterface-hez.

### Metódusok

#### `__init__()`

```python
def __init__(self) -> None
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `register_instance()`

```python
def register_instance(self, interface: Any, instance: Any) -> None
```

**Paraméterek:**

- **`self`**
- **`interface`** (`Any`)
- **`instance`** (`Any`)

**Visszatérési érték:**

- Típus: `None`

#### `register_factory()`

```python
def register_factory(self, interface: Any, factory: Any) -> None
```

**Paraméterek:**

- **`self`**
- **`interface`** (`Any`)
- **`factory`** (`Any`)

**Visszatérési érték:**

- Típus: `None`

#### `resolve()`

```python
def resolve(self, interface: Any) -> Any | None
```

**Paraméterek:**

- **`self`**
- **`interface`** (`Any`)

**Visszatérési érték:**

- Típus: `Any | None`

#### `register_lazy()`

```python
def register_lazy(self, component_name: str, factory_func: Any) -> None
```

**Paraméterek:**

- **`self`**
- **`component_name`** (`str`)
- **`factory_func`** (`Any`)

**Visszatérési érték:**

- Típus: `None`

#### `get()`

```python
def get(self, component_name: str) -> object
```

**Paraméterek:**

- **`self`**
- **`component_name`** (`str`)

**Visszatérési érték:**

- Típus: `object`

#### `clear()`

```python
def clear(self) -> None
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestDIContainerInterface`

DIContainerInterface interfész tesztjei.

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

#### `test_interface_methods_are_callable()`

```python
def test_interface_methods_are_callable(self) -> None
```

Teszteli, hogy az interfész metódusai hívhatók-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_interface_uses_generic_types()`

```python
def test_interface_uses_generic_types(self) -> None
```

Teszteli, hogy az interfész generikus típusokat használ.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_mock_implementation_register_instance()`

```python
def test_mock_implementation_register_instance(self) -> None
```

Teszteli a register_instance metódust mock implementációval (29. sor).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `MockLazyComponent(LazyComponentInterface)`

Mock implementáció a LazyComponentInterface-hez.

### Metódusok

#### `__init__()`

```python
def __init__(self) -> None
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `get()`

```python
def get(self) -> object
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `object`

#### `is_loaded()`

```python
def is_loaded(self) -> bool
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `bool`

## Osztály: `MockLazyComponent(LazyComponentInterface)`

Mock implementáció a LazyComponentInterface-hez.

### Metódusok

#### `__init__()`

```python
def __init__(self) -> None
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `get()`

```python
def get(self) -> object
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `object`

#### `is_loaded()`

```python
def is_loaded(self) -> bool
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `bool`

## Osztály: `TestLazyComponentInterface`

LazyComponentInterface interfész tesztjei.

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

#### `test_interface_methods_are_callable()`

```python
def test_interface_methods_are_callable(self) -> None
```

Teszteli, hogy az interfész metódusai hívhatók-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_interface_defines_lazy_loading_contract()`

```python
def test_interface_defines_lazy_loading_contract(self) -> None
```

Teszteli, hogy az interfész definiálja-e a lusta betöltés szerződését.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_mock_implementation_get()`

```python
def test_mock_implementation_get(self) -> None
```

Teszteli a get metódust mock implementációval (101. sor).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_mock_implementation_register_factory()`

```python
def test_mock_implementation_register_factory(self) -> None
```

Teszteli a register_factory metódust mock implementációval (39. sor).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `factory_func()`

```python
def factory_func() -> str
```

**Visszatérési érték:**

- Típus: `str`

### `test_mock_implementation_resolve()`

```python
def test_mock_implementation_resolve(self) -> None
```

Teszteli a resolve metódust mock implementációval (51. sor).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_mock_implementation_register_lazy()`

```python
def test_mock_implementation_register_lazy(self) -> None
```

Teszteli a register_lazy metódust mock implementációval (64. sor).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `factory_func()`

```python
def factory_func() -> str
```

**Visszatérési érték:**

- Típus: `str`

### `test_mock_implementation_get()`

```python
def test_mock_implementation_get(self) -> None
```

Teszteli a get metódust mock implementációval (79. sor).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `factory_func()`

```python
def factory_func() -> str
```

**Visszatérési érték:**

- Típus: `str`

### `test_mock_implementation_clear()`

```python
def test_mock_implementation_clear(self) -> None
```

Teszteli a clear metódust mock implementációval (84. sor).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_mock_implementation_is_loaded()`

```python
def test_mock_implementation_is_loaded(self) -> None
```

Teszteli az is_loaded property-t mock implementációval (111. sor).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/core/base/interfaces/test_container_interface.py`](../../tests/neural_ai/core/base/interfaces/test_container_interface.py)
