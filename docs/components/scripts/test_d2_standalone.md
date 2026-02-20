# scripts/test_d2_standalone.py

D2 Support Processor standalone teszt script.

Ez a script közvetlenül teszteli a D02SupportProcessor-t a teljes rendszer megkerülése nélkül.
Bootstrap-peli a core komponenseket, majd betölti és feldolgozza az adatokat.

Használat:
    python scripts/test_d2_standalone.py

Author: Neural AI Next Team
Version: 1.0.0

## Importok

```python
import asyncio
import sys
from datetime import UTC
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING
from typing import cast
import polars
from neural_ai.core import bootstrap_core
from neural_ai.data.storage.implementations.parquet_storage import ParquetStorageService
# ... és még 2 import
```

## Konstansok

- **`core`**
: `bootstrap_core()`


- **`symbol`**
: `'EURUSD'`


- **`start_date`**
: `datetime(2023, 1, 1, tzinfo=UTC)`


- **`end_date`**
: `datetime(2023, 1, 2, tzinfo=UTC)`


- **`storage`**
: `cast(ParquetStorageService, core.storage)`


- **`df`**
: `await storage.read_tick_data(symbol, start_date, end_date)`


- **`resampler`**
: `ResamplerServiceFactory.create(core.storage, core.logger)`


- **`ohlcv`**
: `resampler._convert_to_ohlcv(df, '1h')`


- **`ohlcv`**
: `ohlcv.with_columns(high=pl.col('bid_high'), low=pl.col('bid_low'), open=pl.col('bid_open'), close=pl.col('bid_close'))`


- **`processor`**
: `D02SupportFactory.create(core.config, core.logger)`


- **`result`**
: `processor.process(ohlcv, timeframe='H1')`


- **`swing_high_body_count`**
: `result['swing_high_body'].drop_nulls().len()`


- **`swing_low_body_count`**
: `result['swing_low_body'].drop_nulls().len()`


- **`swing_high_wick_count`**
: `result['swing_high_wick'].drop_nulls().len()`


- **`swing_low_wick_count`**
: `result['swing_low_wick'].drop_nulls().len()`


- **`swing_rows`**
: `result.filter(pl.col('swing_high_body').is_not_null() | pl.col('swing_low_body').is_not_null() | pl.col('swing_high_wick').is_not_null() | pl.col('swing_low_wick').is_not_null()).head(5)`


### `run_d2_test()`

```python
async def run_d2_test() -> None
```

D2 Support Processor standalone teszt futtatása. A teszt a következő lépéseket hajtja végre: 1. Core komponensek inicializálása 2. Tick adatok betöltése az adatbázisból 3. Adatok átalakítása H1 OHLCV gyertyákká 4. D2 Support Processor futtatása 5. Eredmények kiírása konzolra

**Visszatérési érték:**

- Típus: `None`

### `main()`

```python
async def main() -> None
```

Főprogram belépési pont.

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`scripts/test_d2_standalone.py`](../../scripts/test_d2_standalone.py)
