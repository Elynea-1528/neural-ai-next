# tests/neural_ai/core/utils/interfaces/test_hardware_interface.py

Hardware interfész tesztelése.

Ez a modul tartalmazza a HardwareInterface interfész egységtesztjeit.

## Importok

```python
import pytest
from neural_ai.core.utils.interfaces.hardware_interface import HardwareInterface
```

## Konstansok

- **`mock_hardware`**
: `MockHardware()`


- **`features`**
: `mock_hardware.get_cpu_features()`


## Osztály: `MockHardware(HardwareInterface)`

Mock implementáció a HardwareInterface-hez.

### Metódusok

#### `__init__()`

```python
def __init__(self) -> None
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `has_avx2()`

```python
def has_avx2(self) -> bool
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `bool`

#### `get_cpu_features()`

```python
def get_cpu_features(self) -> set[str]
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `set[str]`

#### `supports_simd()`

```python
def supports_simd(self) -> bool
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `bool`

## Osztály: `TestHardwareInterface`

HardwareInterface interfész tesztjei.

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

#### `test_all_abstract_methods_implemented()`

```python
def test_all_abstract_methods_implemented(self) -> None
```

Teszteli, hogy az összes absztrakt metódus implementálva van-e a mockban.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/core/utils/interfaces/test_hardware_interface.py`](../../tests/neural_ai/core/utils/interfaces/test_hardware_interface.py)
