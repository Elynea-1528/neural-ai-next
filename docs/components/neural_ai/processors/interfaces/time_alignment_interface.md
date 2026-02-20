# neural_ai/processors/interfaces/time_alignment_interface.py

Időszinkronizációs interfész modul.

## Importok

```python
from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING
import polars
```

## Osztály: `ITimeAlignmentService(ABC)`

Időszinkronizációs szolgáltatás interfész - tökéletes időskála biztosítása.

### Metódusok

#### `reindex_to_grid()`

```python
def reindex_to_grid(self, df: 'pl.DataFrame', timeframe: str) -> 'pl.DataFrame'
```

Tökéletes időskála generálása minden timeframe-re.

**Paraméterek:**

- **`self`**
- **`df`** (`'pl.DataFrame'`)
- **`timeframe`** (`str`)

**Visszatérési érték:**

- Típus: `'pl.DataFrame'`

#### `handle_gaps()`

```python
def handle_gaps(self, df: 'pl.DataFrame', timeframe: str, method: str = 'forward_fill') -> 'pl.DataFrame'
```

Lyukak kezelése az adatokban.

**Paraméterek:**

- **`self`**
- **`df`** (`'pl.DataFrame'`)
- **`timeframe`** (`str`)
- **`method`** (`str`) = `'forward_fill'`

**Visszatérési érték:**

- Típus: `'pl.DataFrame'`

---

**Forrásfájl:** [`neural_ai/processors/interfaces/time_alignment_interface.py`](../../neural_ai/processors/interfaces/time_alignment_interface.py)
