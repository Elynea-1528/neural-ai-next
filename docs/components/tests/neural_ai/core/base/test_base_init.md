# tests/neural_ai/core/base/test_base_init.py

Core base modul __init__.py tesztelése.

Ez a modul teszteli a neural_ai.core.base.__init__.py fájlban
definiált exportokat és funkcionalitásokat.

## Importok

```python
from neural_ai.core.base import CoreComponentFactory
from neural_ai.core.base import CoreComponents
from neural_ai.core.base import DIContainer
from neural_ai.core.base import __all__
import neural_ai.core.base
```

## Osztály: `TestBaseInit`

Base modul __init__.py tesztjei.

### Metódusok

#### `test_dicontainer_import()`

```python
def test_dicontainer_import(self) -> None
```

Teszteli, hogy a DIContainer importálható-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_core_components_import()`

```python
def test_core_components_import(self) -> None
```

Teszteli, hogy a CoreComponents importálható-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_core_component_factory_import()`

```python
def test_core_component_factory_import(self) -> None
```

Teszteli, hogy a CoreComponentFactory importálható-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_all_exports_available()`

```python
def test_all_exports_available(self) -> None
```

Teszteli, hogy minden exportált osztály elérhető-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_type_checking_imports()`

```python
def test_type_checking_imports(self) -> None
```

Teszteli, hogy a TYPE_CHECKING blokkban lévő importok nem okoznak hibát.

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

#### `test_core_components_instantiation()`

```python
def test_core_components_instantiation(self) -> None
```

Teszteli, hogy a CoreComponents példányosítható-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_core_component_factory_instantiation()`

```python
def test_core_component_factory_instantiation(self) -> None
```

Teszteli, hogy a CoreComponentFactory példányosítható-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/core/base/test_base_init.py`](../../tests/neural_ai/core/base/test_base_init.py)
