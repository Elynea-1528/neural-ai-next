# neural_ai/processors/resampler_service/interfaces/resampler_interface.py

ResamplerService Interface - Tick adatokból OHLCV gyertyák létrehozásáért felelős.

## Importok

```python
from abc import ABC
from abc import abstractmethod
from datetime import datetime
from typing import TYPE_CHECKING
import polars
```

## Osztály: `ResamplerInterface(ABC)`

ResamplerService interfész, amely definiálja a tick adatok OHLCV gyertyákká alakítását.

### Metódusok

#### `resample()`

```python
async def resample(self, symbol: str, start: datetime, end: datetime, timeframe: str = '1m', return_type: str = 'polars') -> 'pl.DataFrame'
```

Tick adatok átalakítása OHLCV gyertyákká a megadott időkeretben.

**Paraméterek:**

- **`self`**
- **`symbol`** (`str`): A kereskedési szimbólum (pl. 'EURUSD')
- **`start`** (`datetime`): A kezdő időpont
- **`end`** (`datetime`): A záró időpont
- **`timeframe`** (`str`) = `'1m'`: Az időkeret (alapértelmezett: '1m' - 1 perc)
- **`return_type`** (`str`) = `'polars'`: A visszaadott DataFrame típusa ('pandas' vagy 'polars')

**Visszatérési érték:**

- Típus: `'pl.DataFrame'`
- pl.DataFrame: OHLCV gyertyákat tartalmazó Polars DataFrame

**Kivételek:**

- **`ResamplerError`**: Ha hiba történik az átalakítás során

---

**Forrásfájl:** [`neural_ai/processors/resampler_service/interfaces/resampler_interface.py`](../../neural_ai/processors/resampler_service/interfaces/resampler_interface.py)
