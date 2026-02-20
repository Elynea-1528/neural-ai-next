# tests/neural_ai/core/base/interfaces/test_interfaces_init.py

Core base interfaces modul __init__.py tesztelése.

Ez a modul teszteli a neural_ai.core.base.interfaces.__init__.py fájlban
definiált exportokat és funkcionalitásokat.

## Importok

```python
from neural_ai.core.base.interfaces import CoreComponentFactoryInterface
from neural_ai.core.base.interfaces import CoreComponentsInterface
from neural_ai.core.base.interfaces import DIContainerInterface
from neural_ai.core.base.interfaces import LazyComponentInterface
from neural_ai.core.base.interfaces import __all__
import inspect
import pytest
```

## Osztály: `TestInterfacesInit`

Interfaces modul __init__.py tesztjei.

### Metódusok

#### `test_dicontainer_interface_import()`

```python
def test_dicontainer_interface_import(self) -> None
```

Teszteli, hogy a DIContainerInterface importálható-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_lazy_component_interface_import()`

```python
def test_lazy_component_interface_import(self) -> None
```

Teszteli, hogy a LazyComponentInterface importálható-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_core_components_interface_import()`

```python
def test_core_components_interface_import(self) -> None
```

Teszteli, hogy a CoreComponentsInterface importálható-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_core_component_factory_interface_import()`

```python
def test_core_component_factory_interface_import(self) -> None
```

Teszteli, hogy a CoreComponentFactoryInterface importálható-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_all_exports_available()`

```python
def test_all_exports_available(self) -> None
```

Teszteli, hogy minden exportált interfész elérhető-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_interfaces_are_abstract()`

```python
def test_interfaces_are_abstract(self) -> None
```

Teszteli, hogy az interfészek absztraktak-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_dicontainer_interface_methods()`

```python
def test_dicontainer_interface_methods(self) -> None
```

Teszteli, hogy a DIContainerInterface rendelkezik a szükséges metódusokkal.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_lazy_component_interface_methods()`

```python
def test_lazy_component_interface_methods(self) -> None
```

Teszteli, hogy a LazyComponentInterface rendelkezik a szükséges metódusokkal.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_core_components_interface_methods()`

```python
def test_core_components_interface_methods(self) -> None
```

Teszteli, hogy a CoreComponentsInterface rendelkezik a szükséges metódusokkal.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_core_component_factory_interface_methods()`

```python
def test_core_component_factory_interface_methods(self) -> None
```

Teszteli, hogy a CoreComponentFactoryInterface rendelkezik a szükséges metódusokkal.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_interfaces_cannot_be_instantiated()`

```python
def test_interfaces_cannot_be_instantiated(self) -> None
```

Teszteli, hogy az interfészek nem példányosíthatók.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_interface_methods_are_abstract()`

```python
def test_interface_methods_are_abstract(self) -> None
```

Teszteli, hogy az interfész metódusok absztraktak-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/core/base/interfaces/test_interfaces_init.py`](../../tests/neural_ai/core/base/interfaces/test_interfaces_init.py)
