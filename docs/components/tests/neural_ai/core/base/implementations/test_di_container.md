# tests/neural_ai/core/base/implementations/test_di_container.py

Dependency injection konténer tesztjei.

## Importok

```python
import pytest
from neural_ai.core.base.exceptions import ComponentNotFoundError
from neural_ai.core.base.implementations.di_container import DIContainer
from neural_ai.core.base.implementations.di_container import LazyComponent
from neural_ai.core.base.implementations.di_container import LazyComponent
from neural_ai.core.base.exceptions import ComponentNotFoundError
from neural_ai.core.base.exceptions import SingletonViolationError
```

## Osztály: `MockComponent`

Mock komponens teszteléshez.

### Metódusok

#### `__init__()`

```python
def __init__(self, value: str = 'test') -> None
```

Inicializálja a mock komponenst.

**Paraméterek:**

- **`self`**
- **`value`** (`str`) = `'test'`

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestLazyComponent`

LazyComponent tesztjei.

### Metódusok

#### `test_initialization()`

```python
def test_initialization(self) -> None
```

Teszteli a lusta komponens inicializálását.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `factory()`

```python
def factory() -> MockComponent
```

**Visszatérési érték:**

- Típus: `MockComponent`

#### `test_get_multiple_times()`

```python
def test_get_multiple_times(self) -> None
```

Teszteli a többszöri get hívást.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `factory()`

```python
def factory() -> MockComponent
```

**Visszatérési érték:**

- Típus: `MockComponent`

#### `test_lazy_component_factory_returns_none()`

```python
def test_lazy_component_factory_returns_none(self) -> None
```

LazyComponent factory_func None visszatérése → ComponentNotFoundError

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestDIContainer`

DIContainer tesztjei.

### Metódusok

#### `test_initialization()`

```python
def test_initialization(self) -> None
```

Teszteli a konténer inicializálását.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_register_instance()`

```python
def test_register_instance(self) -> None
```

Teszteli az instance regisztrálását.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_register_factory()`

```python
def test_register_factory(self) -> None
```

Teszteli a factory regisztrálását.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `factory()`

```python
def factory() -> MockComponent
```

**Visszatérési érték:**

- Típus: `MockComponent`

#### `test_resolve_instance()`

```python
def test_resolve_instance(self) -> None
```

Teszteli az instance feloldását.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_resolve_factory()`

```python
def test_resolve_factory(self) -> None
```

Teszteli a factory feloldását.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `factory()`

```python
def factory() -> MockComponent
```

**Visszatérési érték:**

- Típus: `MockComponent`

#### `test_resolve_not_found()`

```python
def test_resolve_not_found(self) -> None
```

Teszteli a nem létező komponens feloldását.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_register_lazy()`

```python
def test_register_lazy(self) -> None
```

Teszteli a lusta komponens regisztrálását.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `factory()`

```python
def factory() -> MockComponent
```

**Visszatérési érték:**

- Típus: `MockComponent`

#### `test_register_lazy_invalid_name()`

```python
def test_register_lazy_invalid_name(self) -> None
```

Teszteli az érvénytelen névvel való regisztrálást.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_register_lazy_invalid_factory()`

```python
def test_register_lazy_invalid_factory(self) -> None
```

Teszteli az érvénytelen factory-val való regisztrálást.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_regular_instance()`

```python
def test_get_regular_instance(self) -> None
```

Teszteli a reguláris instance lekérését.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_lazy_component()`

```python
def test_get_lazy_component(self) -> None
```

Teszteli a lusta komponens lekérését.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `factory()`

```python
def factory() -> MockComponent
```

**Visszatérési érték:**

- Típus: `MockComponent`

#### `test_get_not_found()`

```python
def test_get_not_found(self) -> None
```

Teszteli a nem létező komponens lekérését.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_lazy_components_status()`

```python
def test_get_lazy_components_status(self) -> None
```

Teszteli a lusta komponensek státuszának lekérését.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `factory1()`

```python
def factory1() -> MockComponent
```

**Visszatérési érték:**

- Típus: `MockComponent`

#### `factory2()`

```python
def factory2() -> MockComponent
```

**Visszatérési érték:**

- Típus: `MockComponent`

#### `test_preload_components()`

```python
def test_preload_components(self) -> None
```

Teszteli a komponensek előtöltését.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `factory()`

```python
def factory() -> MockComponent
```

**Visszatérési érték:**

- Típus: `MockComponent`

#### `test_preload_components_not_found()`

```python
def test_preload_components_not_found(self) -> None
```

Teszteli a komponensek előtöltését nem létező komponenssel.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_clear()`

```python
def test_clear(self) -> None
```

Teszteli a konténer ürítését.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_register_method()`

```python
def test_register_method(self) -> None
```

Teszteli a register metódust.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_register_invalid_name()`

```python
def test_register_invalid_name(self) -> None
```

Teszteli az érvénytelen névvel való regisztrálást.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_register_none_instance()`

```python
def test_register_none_instance(self) -> None
```

Teszteli a None instance regisztrálását.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_enforce_singleton_violation()`

```python
def test_enforce_singleton_violation(self) -> None
```

Teszteli a singleton megsértését.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_enforce_singleton_no_violation()`

```python
def test_enforce_singleton_no_violation(self) -> None
```

Teszteli, hogy azonos instance regisztrálása nem okoz problémát.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_memory_usage()`

```python
def test_get_memory_usage(self) -> None
```

Teszteli a memória használat lekérését.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/core/base/implementations/test_di_container.py`](../../tests/neural_ai/core/base/implementations/test_di_container.py)
