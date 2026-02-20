# neural_ai/processors/resampler_service/implementations/resampler_service.py

ResamplerService implementáció - Tick adatokból OHLCV gyertyák létrehozása.

## Importok

```python
from datetime import datetime
from typing import TYPE_CHECKING
from typing import Union
import polars
import pandas
from neural_ai.processors.resampler_service.exceptions.resampler_error import DataLoadError
from neural_ai.processors.resampler_service.exceptions.resampler_error import InvalidTimeframeError
from neural_ai.processors.resampler_service.exceptions.resampler_error import ResamplingError
from neural_ai.processors.resampler_service.interfaces.resampler_interface import ResamplerInterface
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
# ... és még 1 import
```

## Osztály: `ResamplerService(ResamplerInterface)`

ResamplerService implementáció, amely tick adatokból hoz létre OHLCV gyertyákat.

Ez a szolgáltatás felelős a tick adatok átalakításáért OHLCV (Open, High, Low, Close, Volume)
gyertyákká a megadott időkeretben. A hatékonyság érdekében Polars-t használ.

### Metódusok

#### `__init__()`

```python
def __init__(self, storage: 'StorageInterface', logger: 'LoggerInterface') -> None
```

ResamplerService inicializálása.

**Paraméterek:**

- **`self`**
- **`storage`** (`'StorageInterface'`): A tárolási interfész példány (Dependency Injection)
- **`logger`** (`'LoggerInterface'`): A naplózási interfész (Dependency Injection)

**Visszatérési érték:**

- Típus: `None`

#### `resample()`

```python
async def resample(self, symbol: str, start: datetime, end: datetime, timeframe: str = '1m', return_type: str = 'polars') -> Union[pl.DataFrame, 'pd.DataFrame']
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

- Típus: `Union[pl.DataFrame, 'pd.DataFrame']`
- Union[pl.DataFrame, pd.DataFrame]: OHLCV gyertyákat tartalmazó DataFrame

**Kivételek:**

- **`InvalidTimeframeError`**: Ha az időkeret érvénytelen
- **`DataLoadError`**: Ha hiba történik az adatok betöltése során
- **`ResamplingError`**: Ha hiba történik az átalakítás során

#### `_validate_timeframe()`

```python
def _validate_timeframe(self, timeframe: str) -> None
```

Időkeret validálása.

**Paraméterek:**

- **`self`**
- **`timeframe`** (`str`): Az időkeret string

**Visszatérési érték:**

- Típus: `None`

**Kivételek:**

- **`InvalidTimeframeError`**: Ha az időkeret érvénytelen

#### `_load_tick_data()`

```python
async def _load_tick_data(self, symbol: str, start: datetime, end: datetime) -> pl.DataFrame
```

Tick adatok betöltése a tárolóból.

**Paraméterek:**

- **`self`**
- **`symbol`** (`str`): A kereskedési szimbólum
- **`start`** (`datetime`): A kezdő időpont
- **`end`** (`datetime`): A záró időpont

**Visszatérési érték:**

- Típus: `pl.DataFrame`
- Polars DataFrame a tick adatokkal

**Kivételek:**

- **`DataLoadError`**: Ha hiba történik a betöltés során

#### `_convert_to_ohlcv()`

```python
def _convert_to_ohlcv(self, tick_data: pl.DataFrame, timeframe: str) -> pl.DataFrame
```

Tick adatok átalakítása kiterjesztett OHLCV gyertyákká.

**Paraméterek:**

- **`self`**
- **`tick_data`** (`pl.DataFrame`): Polars DataFrame tick adatokkal
- **`timeframe`** (`str`): Az időkeret

**Visszatérési érték:**

- Típus: `pl.DataFrame`
- Polars DataFrame kiterjesztett gyertyákkal (Bid/Mid OHLC, Spread, Real/Tick Volume)

---

**Forrásfájl:** [`neural_ai/processors/resampler_service/implementations/resampler_service.py`](../../neural_ai/processors/resampler_service/implementations/resampler_service.py)
