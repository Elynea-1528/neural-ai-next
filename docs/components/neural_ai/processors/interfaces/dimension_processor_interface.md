# neural_ai/processors/interfaces/dimension_processor_interface.py

Dimenzió processzor interfész modul.

## Importok

```python
from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING
import polars
```

## Osztály: `IDimensionProcessor(ABC)`

Absztrakt interfész minden dimenzió processzor számára.

### Metódusok

#### `process()`

```python
def process(self, df: 'pl.DataFrame') -> 'pl.DataFrame'
```

Polars Expr alapú dimenzió számítás.

**Paraméterek:**

- **`self`**
- **`df`** (`'pl.DataFrame'`)

**Visszatérési érték:**

- Típus: `'pl.DataFrame'`

#### `dimension_id()`

```python
def dimension_id(self) -> int
```

Dimenzió azonosító (1-15).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `int`

---

**Forrásfájl:** [`neural_ai/processors/interfaces/dimension_processor_interface.py`](../../neural_ai/processors/interfaces/dimension_processor_interface.py)
