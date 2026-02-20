# tests/neural_ai/core/base/implementations/test_implementations_init.py

Core base implementations modul __init__.py tesztelése.

Ez a modul teszteli a neural_ai.core.base.implementations.__init__.py fájlban
definiált exportokat és funkcionalitásokat.

## Importok

```python
from neural_ai.core.base.implementations import DIContainer
from neural_ai.core.base.implementations import LazyComponent
from neural_ai.core.base.implementations import LazyLoader
from neural_ai.core.base.implementations import SingletonMeta
from neural_ai.core.base.implementations import lazy_property
from neural_ai.core.base.implementations.component_bundle import CoreComponents
from neural_ai.core.base.implementations import __all__
```

## Konstansok

- **`obj1`**
: `TestClass()`


- **`obj2`**
: `TestClass()`


- **`obj`**
: `TestClass()`


- **`result1`**
: `obj.expensive_value`


- **`result2`**
: `obj.expensive_value`


## Osztály: `TestClass`

### Metódusok

#### `__init__()`

```python
def __init__(self) -> None
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestClass`

### Metódusok

#### `__init__()`

```python
def __init__(self) -> None
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `expensive_value()`

```python
def expensive_value(self) -> str
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `str`

## Osztály: `TestImplementationsInit`

Implementations modul __init__.py tesztjei.

### Metódusok

#### `test_core_components_import()`

```python
def test_core_components_import(self) -> None
```

Teszteli, hogy a CoreComponents importálható-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_dicontainer_import()`

```python
def test_dicontainer_import(self) -> None
```

Teszteli, hogy a DIContainer importálható-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_lazy_component_import()`

```python
def test_lazy_component_import(self) -> None
```

Teszteli, hogy a LazyComponent importálható-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_lazy_loader_import()`

```python
def test_lazy_loader_import(self) -> None
```

Teszteli, hogy a LazyLoader importálható-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_lazy_property_import()`

```python
def test_lazy_property_import(self) -> None
```

Teszteli, hogy a lazy_property importálható-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_singleton_meta_import()`

```python
def test_singleton_meta_import(self) -> None
```

Teszteli, hogy a SingletonMeta importálható-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_all_exports_available()`

```python
def test_all_exports_available(self) -> None
```

Teszteli, hogy minden exportált osztály/függvény elérhető-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_core_components_instantiation()`

```python
def test_core_components_instantiation(self) -> None
```

Teszteli, hogy a CoreComponents példányosítható-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_dicontainer_instantiation()`

```python
def test_dicontainer_instantiation(self) -> None
```

Teszteli, hogy a DIContainer példányosítható-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_lazy_component_instantiation()`

```python
def test_lazy_component_instantiation(self) -> None
```

Teszteli, hogy a LazyComponent példányosítható-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `factory_func()`

```python
def factory_func() -> str
```

**Visszatérési érték:**

- Típus: `str`

#### `test_lazy_loader_instantiation()`

```python
def test_lazy_loader_instantiation(self) -> None
```

Teszteli, hogy a LazyLoader példányosítható-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `loader_func()`

```python
def loader_func() -> str
```

**Visszatérési érték:**

- Típus: `str`

#### `test_singleton_meta_as_metaclass()`

```python
def test_singleton_meta_as_metaclass(self) -> None
```

Teszteli, hogy a SingletonMeta használható-e metaclass-ként.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_lazy_property_decorator()`

```python
def test_lazy_property_decorator(self) -> None
```

Teszteli, hogy a lazy_property dekorátor használható-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/core/base/implementations/test_implementations_init.py`](../../tests/neural_ai/core/base/implementations/test_implementations_init.py)
