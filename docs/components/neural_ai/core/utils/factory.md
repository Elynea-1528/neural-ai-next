# neural_ai/core/utils/factory.py

Hardverinformációk lekérdezéséhez szükséges Factory osztály.

Ez a modul a `HardwareFactory` osztályt tartalmazza, amely a
`HardwareInfo` implementáció példányosításáért felelős.

## Importok

```python
from typing import TYPE_CHECKING
from neural_ai.core.utils.implementations.hardware_info import HardwareInfo
from neural_ai.core.utils.interfaces.hardware_interface import HardwareInterface
from neural_ai.core.utils.implementations.hardware_info import HardwareInfo
from neural_ai.core.utils.implementations.hardware_info import HardwareInfo
```

## Osztály: `HardwareFactory`

Factory osztály a `HardwareInfo` példányosításához.

### Metódusok

#### `get_hardware_info()`

```python
def get_hardware_info() -> 'HardwareInfo'
```

Visszaad egy `HardwareInfo` példányt.

**Visszatérési érték:**

- Típus: `'HardwareInfo'`
- HardwareInfo: A hardverinformációkat tartalmazó osztály példánya.

#### `get_hardware_interface()`

```python
def get_hardware_interface() -> 'HardwareInterface'
```

Visszaad egy `HardwareInterface`-t implementáló példányt.

**Visszatérési érték:**

- Típus: `'HardwareInterface'`
- HardwareInterface: A hardverinterfészt implementáló osztály példánya.

---

**Forrásfájl:** [`neural_ai/core/utils/factory.py`](../../neural_ai/core/utils/factory.py)
