# tests/neural_ai/core/utils/test_utils_factory.py

Tesztek a HardwareFactory osztályhoz.

Ez a modul a `HardwareFactory` osztály tesztjeit tartalmazza, amelyek ellenőrzik
a hardverinformációk lekérdezéséhez szükséges factory metódusok helyes működését.

## Importok

```python
from unittest.mock import MagicMock
from unittest.mock import patch
import pytest
from neural_ai.core.utils.factory import HardwareFactory
from neural_ai.core.utils.interfaces.hardware_interface import HardwareInterface
import inspect
```

## Osztály: `TestHardwareFactory`

Tesztosztály a HardwareFactory metódusainak teszteléséhez.

### Metódusok

#### `test_get_hardware_info_returns_hardware_info_instance()`

```python
def test_get_hardware_info_returns_hardware_info_instance(self) -> None
```

Teszteli, hogy a get_hardware_info visszaad-e HardwareInfo példányt.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_hardware_info_returns_new_instance()`

```python
def test_get_hardware_info_returns_new_instance(self) -> None
```

Teszteli, hogy a get_hardware_info mindig új példányt ad-e vissza.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_hardware_interface_returns_hardware_interface()`

```python
def test_get_hardware_interface_returns_hardware_interface(self) -> None
```

Teszteli, hogy a get_hardware_interface visszaad-e HardwareInterface-t.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_hardware_interface_returns_new_instance()`

```python
def test_get_hardware_interface_returns_new_instance(self) -> None
```

Teszteli, hogy a get_hardware_interface mindig új példányt ad-e vissza.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_hardware_info_and_interface_return_different_instances()`

```python
def test_get_hardware_info_and_interface_return_different_instances(self) -> None
```

Teszteli, hogy a factory különböző példányokat ad-e vissza.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_hardware_info_implements_hardware_interface()`

```python
def test_hardware_info_implements_hardware_interface(self) -> None
```

Teszteli, hogy a HardwareInfo implementálja-e a HardwareInterface-t.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_hardware_info_imports_correctly()`

```python
def test_get_hardware_info_imports_correctly(self, mock_hardware_info: MagicMock) -> None
```

Teszteli, hogy a get_hardware_info helyesen importálja-e a HardwareInfo osztályt.

**Paraméterek:**

- **`self`**
- **`mock_hardware_info`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_get_hardware_interface_imports_correctly()`

```python
def test_get_hardware_interface_imports_correctly(self, mock_hardware_info: MagicMock) -> None
```

Teszteli, hogy a get_hardware_interface helyesen importálja-e a HardwareInfo osztályt.

**Paraméterek:**

- **`self`**
- **`mock_hardware_info`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_factory_methods_are_static()`

```python
def test_factory_methods_are_static(self) -> None
```

Teszteli, hogy a factory metódusok statikusak-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestHardwareFactoryIntegration`

Integrációs tesztek a HardwareFactory-hez.

### Metódusok

#### `test_factory_creates_working_hardware_info_instance()`

```python
def test_factory_creates_working_hardware_info_instance(self) -> None
```

Teszteli, hogy a factory által létrehozott példány működőképes-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_factory_creates_working_hardware_interface()`

```python
def test_factory_creates_working_hardware_interface(self) -> None
```

Teszteli, hogy a factory által létrehozott interfész működőképes-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/core/utils/test_utils_factory.py`](../../tests/neural_ai/core/utils/test_utils_factory.py)
