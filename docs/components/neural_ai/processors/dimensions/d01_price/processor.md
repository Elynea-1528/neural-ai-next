# neural_ai/processors/dimensions/d01_price/processor.py

D01PriceProcessor - Alap adatok processzor.

## Importok

```python
from typing import TYPE_CHECKING
import polars
from neural_ai.processors.dimensions.base import BaseDimensionProcessor
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
```

## Osztály: `D01PriceProcessor(BaseDimensionProcessor)`

D1 - Alap adatok (Base Data) processzor.

Feladata az alap pénzügyi adatok biztosítása és validálása.
Kiválasztja és visszaadja a timestamp, open, high, low, close,
tick_volume, spread és real_volume oszlopokat.

### Metódusok

#### `__init__()`

```python
def __init__(self, config: 'ConfigManagerInterface', logger: 'LoggerInterface') -> None
```

Inicializálja a D1 processzort.

**Paraméterek:**

- **`self`**
- **`config`** (`'ConfigManagerInterface'`): Konfigurációs menedzser interfész
- **`logger`** (`'LoggerInterface'`): Logger interfész

**Visszatérési érték:**

- Típus: `None`

#### `process()`

```python
def process(self, df: pl.DataFrame, timeframe: str = '1m') -> pl.DataFrame
```

Polars Expr alapú dimenzió számítás matematikai transzformációkkal. Számítja a log return-ot, rolling Z-score-ot és árnyékokat (shadows). Adaptív logika: tick timeframe esetén különbözik az OHLC-tól.

**Paraméterek:**

- **`self`**
- **`df`** (`pl.DataFrame`): Bemeneti Polars DataFrame (már time-aligned OHLCV adatok)
- **`timeframe`** (`str`) = `'1m'`: Időkeret ("tick", "1m", stb.), default "1m"

**Visszatérési érték:**

- Típus: `pl.DataFrame`
- Polars DataFrame az alap adatokkal és matematikai transzformációkkal

#### `dimension_id()`

```python
def dimension_id(self) -> int
```

Dimenzió azonosító (1-15).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `int`
- int: 1 (D1 dimenzió)

---

**Forrásfájl:** [`neural_ai/processors/dimensions/d01_price/processor.py`](../../neural_ai/processors/dimensions/d01_price/processor.py)
