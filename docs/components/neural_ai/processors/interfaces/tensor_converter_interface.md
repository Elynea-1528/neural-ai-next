# neural_ai/processors/interfaces/tensor_converter_interface.py

Tensor konverter interfész modul.

## Importok

```python
from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING
import numpy
```

## Osztály: `ITensorConverter(ABC)`

Tensor konverter interfész.

### Metódusok

#### `convert_to_tensor()`

```python
def convert_to_tensor(self, data: 'np.ndarray') -> 'np.ndarray'
```

Adatok konvertálása tensor formátumba.

**Paraméterek:**

- **`self`**
- **`data`** (`'np.ndarray'`)

**Visszatérési érték:**

- Típus: `'np.ndarray'`

---

**Forrásfájl:** [`neural_ai/processors/interfaces/tensor_converter_interface.py`](../../neural_ai/processors/interfaces/tensor_converter_interface.py)
