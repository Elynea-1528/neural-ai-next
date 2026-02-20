# scripts/download_history.py

Tömeges tick adat letöltő script a Neural AI Next rendszerhez (DIRECT STORAGE MODE).

Ez a script lehetővé teszi a tick adatok tömeges letöltését a JForex adatforrásból
egy megadott dátumtartományban. A letöltött adatok közvetlenül a ParquetStorageService
által kerülnek mentésre, kikerülve az EventBus-t a maximális sebesség érdekében.

Használat:
    python scripts/download_history.py --symbol EURUSD --start 2023-01-01 --end 2023-12-31

Author: Neural AI Next Team
Version: 2.0.0 (Direct Storage Mode)

## Importok

```python
import argparse
import asyncio
import sys
from datetime import UTC
from datetime import datetime
from datetime import timedelta
from pathlib import Path
from typing import TYPE_CHECKING
from typing import cast
import polars
# ... és még 8 import
```

## Konstansok

- **`core`**
: `bootstrap_core()`


- **`logger`**
: `core.logger`


- **`storage`**
: `cast(ParquetStorageService, core.storage)`


- **`data_dir`**
: `Path('data/tick')`


- **`downloader`**
: `JForexFactory.create_downloader(config=core.config, logger=logger, event_bus=None, storage=storage)`


- **`current_date`**
: `start_date`


- **`total_days`**
: `(end_date - start_date).days + 1`


- **`successful_downloads`**
: `0`


- **`failed_downloads`**
: `0`


- **`skipped_downloads`**
: `0`


- **`total_ticks`**
: `0`


- **`day_count`**
: `0`


- **`current_hour`**
: `current_date.replace(hour=0, minute=0, second=0, microsecond=0)`


- **`end_hour`**
: `current_date.replace(hour=23, minute=0, second=0, microsecond=0)`


- **`hours_downloaded`**
: `0`


- **`hours_failed`**
: `0`


- **`day_ticks`**
: `0`


- **`base_path`**
: `storage.BASE_PATH`


- **`hour_dir`**
: `base_path / symbol.upper() / f'year={current_hour.year}' / f'month={current_hour.month:02d}' / f'day={current_hour.day:02d}'`


- **`master_filename`**
: `f"tick_{current_hour.strftime('%Y%m%d_%H')}.parquet"`


- **`expected_path`**
: `hour_dir / master_filename`


- **`ticks`**
: `await downloader.download_tick_data(symbol, current_hour)`


- **`tick_dicts`**
: `[{'timestamp': tick.timestamp, 'bid': tick.bid, 'ask': tick.ask, 'ask_volume': tick.ask_volume if tick.ask_volume is not None else 0.0, 'bid_volume': tick.bid_volume if tick.bid_volume is not None else 0.0, 'source': 'jforex'} for tick in ticks]`


- **`df`**
: `pl.DataFrame(tick_dicts)`


- **`date_str`**
: `date.strftime('%Y%m%d')`


- **`time_suffix`**
: `date.strftime('%H')`


- **`error_msg`**
: `f'Hiba a tick adatok mentésekor: {e}'`


- **`parser`**
: `argparse.ArgumentParser(description='Történelmi tick adatok letöltése JForex-ről')`


- **`args`**
: `parser.parse_args()`


- **`start_date`**
: `datetime.strptime(args.start, '%Y-%m-%d').replace(tzinfo=UTC)`


- **`end_date`**
: `datetime.strptime(args.end, '%Y-%m-%d').replace(hour=23, minute=59, second=59, tzinfo=UTC)`


### `download_historical_data()`

```python
async def download_historical_data(symbol: str, start_date: datetime, end_date: datetime) -> None
```

Történelmi tick adatok letöltése a megadott tartományban (Direct Storage Mode).

**Paraméterek:**

- **`symbol`** (`str`): A pénzpár szimbóluma (pl. 'EURUSD')
- **`start_date`** (`datetime`): A letöltés kezdő dátuma
- **`end_date`** (`datetime`): A letöltés záró dátuma

**Visszatérési érték:**

- Típus: `None`

### `_save_ticks_direct()`

```python
async def _save_ticks_direct(storage: 'ParquetStorageService', symbol: str, ticks: list['TickData'], date: datetime, logger: 'LoggerInterface | None' = None) -> None
```

Tick adatok közvetlen mentése a storage-ba (Direct Storage Mode).

**Paraméterek:**

- **`storage`** (`'ParquetStorageService'`): A storage interfész (ParquetStorageService)
- **`symbol`** (`str`): A pénzpár szimbóluma
- **`ticks`** (`list['TickData']`): A tick adatok listája
- **`date`** (`datetime`): A dátum
- **`logger`** (`'LoggerInterface | None'`) = `None`: A logger (opcionális)

**Visszatérési érték:**

- Típus: `None`

### `parse_arguments()`

```python
def parse_arguments() -> tuple[str, datetime, datetime]
```

Argumentumok feldolgozása.

**Visszatérési érték:**

- Típus: `tuple[str, datetime, datetime]`
- A feldolgozott argumentumok: (symbol, start_date, end_date)

### `main()`

```python
def main() -> None
```

Főprogram.

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`scripts/download_history.py`](../../scripts/download_history.py)
