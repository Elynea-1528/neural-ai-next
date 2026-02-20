# tests/neural_ai/core/base/implementations/test_singleton.py

SingletonMeta tesztelése.

Ez a modul tartalmazza a SingletonMeta metaclass egységtesztjeit,
beleértve a singleton minta ellenőrzését és a DI kompatibilitást.

## Importok

```python
from neural_ai.core.base.implementations.singleton import SingletonMeta
```

## Konstansok

- **`obj1`**
: `TestClass(42)`


- **`obj2`**
: `TestClass(100)`


- **`obj_a`**
: `ClassA('A')`


- **`obj_b`**
: `ClassB('B')`


- **`obj1`**
: `TestClass(value=42)`


- **`obj2`**
: `TestClass(value=100)`


- **`obj1`**
: `TestClass()`


- **`obj2`**
: `TestClass()`


- **`obj`**
: `TestClass()`


- **`obj1`**
: `TestClass()`


- **`obj2`**
: `TestClass()`


- **`obj1`**
: `TestClass()`


- **`obj2`**
: `TestClass()`


- **`obj1`**
: `TestClass()`


- **`obj2`**
: `TestClass()`


- **`obj1`**
: `TestClass()`


- **`obj2`**
: `TestClass()`


- **`obj1`**
: `TestClass(42)`


- **`obj2`**
: `TestClass(100)`


## Osztály: `TestClass`

### Metódusok

#### `__init__()`

```python
def __init__(self, value: int) -> None
```

**Paraméterek:**

- **`self`**
- **`value`** (`int`)

**Visszatérési érték:**

- Típus: `None`

## Osztály: `ClassA`

### Metódusok

#### `__init__()`

```python
def __init__(self, value: str) -> None
```

**Paraméterek:**

- **`self`**
- **`value`** (`str`)

**Visszatérési érték:**

- Típus: `None`

## Osztály: `ClassB`

### Metódusok

#### `__init__()`

```python
def __init__(self, value: str) -> None
```

**Paraméterek:**

- **`self`**
- **`value`** (`str`)

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestClass`

### Metódusok

#### `__init__()`

```python
def __init__(self, value: int = 0) -> None
```

**Paraméterek:**

- **`self`**
- **`value`** (`int`) = `0`

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

## Osztály: `BaseClass`

### Metódusok

#### `__init__()`

```python
def __init__(self) -> None
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestClass(BaseClass)`

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

#### `get_value()`

```python
def get_value(cls) -> int
```

**Paraméterek:**

- **`cls`**

**Visszatérési érték:**

- Típus: `int`

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
def __init__(self, value: int) -> None
```

**Paraméterek:**

- **`self`**
- **`value`** (`int`)

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestSingletonMeta`

SingletonMeta metaclass tesztjei.

### Metódusok

#### `test_singleton_creates_only_one_instance()`

```python
def test_singleton_creates_only_one_instance(self) -> None
```

Teszteli, hogy csak egy példány jön létre.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_singleton_different_classes()`

```python
def test_singleton_different_classes(self) -> None
```

Teszteli, hogy különböző osztályok külön példányt kapnak.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_singleton_with_kwargs()`

```python
def test_singleton_with_kwargs(self) -> None
```

Teszteli a singleton-t kulcsszavas argumentumokkal.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_singleton_without_args()`

```python
def test_singleton_without_args(self) -> None
```

Teszteli a singleton-t argumentumok nélkül.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_singleton_has_initialized_flag()`

```python
def test_singleton_has_initialized_flag(self) -> None
```

Teszteli, hogy a példánynak van _initialized flag-je (DI kompatibilitás).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_singleton_has_instance_class_variable()`

```python
def test_singleton_has_instance_class_variable(self) -> None
```

Teszteli, hogy az osztálynak van _instance class változója (DI kompatibilitás).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_singleton_multiple_inheritance()`

```python
def test_singleton_multiple_inheritance(self) -> None
```

Teszteli a singleton-t többszörös öröklődés esetén.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_singleton_with_class_method()`

```python
def test_singleton_with_class_method(self) -> None
```

Teszteli a singleton-t osztálymetódussal.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_singleton_instances_dict()`

```python
def test_singleton_instances_dict(self) -> None
```

Teszteli, hogy a singleton tényleg egy példányt hoz létre.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_singleton_reset_behavior()`

```python
def test_singleton_reset_behavior(self) -> None
```

Teszteli, hogy a singleton nem enged második inicializálást.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/core/base/implementations/test_singleton.py`](../../tests/neural_ai/core/base/implementations/test_singleton.py)
