# neural_ai/processors/implementations/time_alignment_service.py

Időszinkronizációs szolgáltatás implementáció.

## Importok

```python
from typing import TYPE_CHECKING
import polars
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
from neural_ai.processors.interfaces.time_alignment_interface import ITimeAlignmentService
```

## Osztály: `TimeAlignmentService(ITimeAlignmentService)`

Időszinkronizációs szolgáltatás - tökéletes időskála biztosítása.

Ez az osztály biztosítja az időszinkronizációs műveleteket, mint a rácsra
indexelés és lyukak kezelése az adatokban.

### Metódusok

#### `__init__()`

```python
def __init__(self, logger: LoggerInterface) -> None
```

Időszinkronizációs szolgáltatás inicializálása.

**Paraméterek:**

- **`self`**
- **`logger`** (`LoggerInterface`): A naplózási interfész a műveletek naplózásához.

**Visszatérési érték:**

- Típus: `None`

#### `reindex_to_grid()`

```python
def reindex_to_grid(self, df: pl.DataFrame, timeframe: str) -> pl.DataFrame
```

Tökéletes időskála generálása minden timeframe-re. Létrehozza az összes szükséges időpontot a megadott timeframe alapján, és kitölti a hiányzó értékeket.

**Paraméterek:**

- **`self`**
- **`df`** (`pl.DataFrame`): A bemeneti DataFrame időbélyegekkel.
- **`timeframe`** (`str`): Az időintervallum (pl. '1m', '5m').

**Visszatérési érték:**

- Típus: `pl.DataFrame`
- pl.DataFrame: Az újragridelt DataFrame.

#### `market_hours_filter()`

```python
def market_hours_filter(self, df: pl.DataFrame) -> pl.DataFrame
```

Hétvégék szűrése - csak H-P napok megtartása, kivétel vasárnap >=21 UTC.

**Paraméterek:**

- **`self`**
- **`df`** (`pl.DataFrame`): A bemeneti DataFrame időbélyegekkel.

**Visszatérési érték:**

- Típus: `pl.DataFrame`
- pl.DataFrame: A szűrt DataFrame piaci órákban.

#### `handle_gaps()`

```python
def handle_gaps(self, df: pl.DataFrame, timeframe: str, method: str = 'forward_fill') -> pl.DataFrame
```

Lyukak kezelése az adatokban - árak forward fill, volumenek 0.

**Paraméterek:**

- **`self`**
- **`df`** (`pl.DataFrame`): A bemeneti DataFrame lyukakkal.
- **`timeframe`** (`str`): Az időintervallum.
- **`method`** (`str`) = `'forward_fill'`: A lyukkezelési módszer ('forward_fill' vagy 'mask').

**Visszatérési érték:**

- Típus: `pl.DataFrame`
- pl.DataFrame: A lyukak nélküli DataFrame.

**Kivételek:**

- **`ValueError`**: Ha ismeretlen method van megadva.

---

**Forrásfájl:** [`neural_ai/processors/implementations/time_alignment_service.py`](../../neural_ai/processors/implementations/time_alignment_service.py)
