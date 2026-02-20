# scripts/validation_end_to_end.py

End-to-End validációs szkript a CORE DATA PIPELINE teljes refaktorálásának ellenőrzésére.

Ez a szkript végrehajtja az összes szükséges lépést a pipeline validálására:
1. Adat letöltés egy napra (EURUSD 2024-03-20)
2. Dashboard indításának ellenőrzése
3. Adatok ellenőrzése a Strategy Service-en keresztül
4. Új oszlopok (mid_open, mid_close, spread, rolling_z_score) validálása

Használat:
    python scripts/validation_end_to_end.py

Author: Neural AI Next Team
Version: 1.0.0

## Importok

```python
import asyncio
import subprocess
import sys
import time
from pathlib import Path
from typing import TYPE_CHECKING
from typing import cast
import polars
import requests
from neural_ai.ui.core_bridge import CoreBridge
# ... és még 5 import
```

## Konstansok

- **`script_path`**
: `Path(__file__).parent / 'download_history.py'`


- **`cmd`**
: `['/home/elynea/miniconda3/envs/neural-ai-next/bin/python', str(script_path), '--symbol', 'EURUSD', '--start', '2024-03-20', '--end', '2024-03-20']`


- **`result`**
: `subprocess.run(cmd, capture_output=True, text=True, timeout=300)`


- **`force_kill_path`**
: `Path(__file__).parent / 'force_kill.py'`


- **`kill_result`**
: `subprocess.run(['/home/elynea/miniconda3/envs/neural-ai-next/bin/python', str(force_kill_path)], capture_output=True, text=True, timeout=30)`


- **`main_path`**
: `Path(__file__).parent.parent / 'main.py'`


- **`cmd`**
: `['/home/elynea/miniconda3/envs/neural-ai-next/bin/python', str(main_path), 'dashboard', '--headless']`


- **`process`**
: `subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=Path(__file__).parent.parent)`


- **`max_wait`**
: `30`


- **`check_interval`**
: `1`


- **`health_url`**
: `'http://localhost:8501/_stcore/health'`


- **`response`**
: `requests.get(health_url, timeout=2)`


- **`bridge`**
: `CoreBridge()`


- **`config`**
: `cast(ConfigManagerInterface, bridge.get_component('config'))`


- **`logger`**
: `cast(LoggerInterface, bridge.get_component('logger'))`


- **`strategy_service`**
: `cast(StrategyServiceInterface, bridge.get_component('strategy_service'))`


- **`d2_processor`**
: `create_dimension_processor(2, config, logger)`


- **`df`**
: `df.clone()`


- **`rename_dict`**
: `{col: col.lower() for col in df.columns}`


- **`df`**
: `df.rename(rename_dict)`


- **`required_columns`**
: `['timestamp', 'bid_open', 'bid_high', 'bid_low', 'bid_close']`


- **`missing_columns`**
: `[col for col in required_columns if col not in df.columns]`


- **`expected_columns`**
: `['swing_high', 'swing_low', 'resistance', 'support']`


- **`missing_new_columns`**
: `[col for col in expected_columns if col not in processed_df.columns]`


- **`swing_high_count`**
: `processed_df.select(pl.col('swing_high').sum()).item()`


- **`swing_low_count`**
: `processed_df.select(pl.col('swing_low').sum()).item()`


- **`resistance_present`**
: `'resistance' in processed_df.columns`


- **`support_present`**
: `'support' in processed_df.columns`


- **`bridge`**
: `CoreBridge()`


- **`strategy_service`**
: `cast(StrategyServiceInterface, bridge.get_component('strategy_service'))`


- **`df`**
: `df.rename({col: col.lower() for col in df.columns})`


- **`required_columns`**
: `['timestamp', 'bid_open', 'bid_high', 'bid_low', 'bid_close', 'mid_close']`


- **`missing_columns`**
: `[col for col in required_columns if col not in df.columns]`


- **`new_columns`**
: `['mid_open', 'mid_high', 'mid_low', 'mid_close', 'spread', 'real_volume', 'tick_volume', 'bid_volume', 'ask_volume']`


- **`missing_new_columns`**
: `[col for col in new_columns if col not in df.columns]`


- **`spread_values`**
: `df['spread'].drop_nulls()`


- **`zscore_values`**
: `df['rolling_z_score'].drop_nulls()`


- **`mid_columns`**
: `['mid_open', 'mid_high', 'mid_low', 'mid_close']`


- **`values`**
: `df[col].drop_nulls()`


- **`bid_open`**
: `df['bid_open']`


- **`mid_open`**
: `df['mid_open']`


- **`success_count`**
: `0`


- **`total_steps`**
: `4`


### `download_data()`

```python
def download_data() -> bool
```

Adat letöltés futtatása EURUSD 2024-03-20-ra.

**Visszatérési érték:**

- Típus: `bool`
- bool: Sikeres volt-e a letöltés

### `test_dashboard_startup()`

```python
def test_dashboard_startup() -> bool
```

Dashboard indításának tesztelése.

**Visszatérési érték:**

- Típus: `bool`
- bool: Sikeres volt-e az indítás

### `validate_d2_swing_engine()`

```python
async def validate_d2_swing_engine() -> bool
```

D2 Swing Engine implementáció validálása.

**Visszatérési érték:**

- Típus: `bool`
- bool: Sikeres volt-e a validáció

### `validate_data()`

```python
async def validate_data() -> bool
```

Adatok validálása a Strategy Service-en keresztül.

**Visszatérési érték:**

- Típus: `bool`
- bool: Sikeres volt-e a validáció

### `main()`

```python
async def main() -> None
```

Fő validációs folyamat.

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`scripts/validation_end_to_end.py`](../../scripts/validation_end_to_end.py)
