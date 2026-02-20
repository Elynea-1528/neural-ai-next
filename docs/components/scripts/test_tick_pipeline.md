# scripts/test_tick_pipeline.py

Tick adatok feldolgozási útvonalának teljes validációja.

Ez a szkript validálja a Resampler és D1 Dimension Processor komponensek
együttműködését "tick" timeframe-mal.

## Importok

```python
from datetime import UTC
from datetime import datetime
from datetime import timedelta
from typing import Any
import polars
from neural_ai.core.config.implementations.yaml_config_manager import YAMLConfigManager
from neural_ai.core.logger.factory import LoggerFactory
from neural_ai.processors.dimensions.d01_price.processor import D01PriceProcessor
```

## Konstansok

- **`logger`**
: `LoggerFactory.get_logger(__name__, logger_type='colored')`


- **`config`**
: `_create_mock_config()`


- **`mock_logger`**
: `_create_mock_logger()`


- **`tick_data`**
: `_generate_test_tick_data()`


- **`resample_result`**
: `_validate_resample(tick_data, mock_logger)`


- **`final_result`**
: `_validate_d1_processor(resample_result, config, mock_logger)`


- **`timestamps`**
: `[datetime(2023, 1, 1, 10, 0, 0, tzinfo=UTC) + timedelta(seconds=i) for i in range(100)]`


- **`bids`**
: `[1.052 + 0.0001 * (i % 10) for i in range(100)]`


- **`asks`**
: `[bid + 0.0002 for bid in bids]`


- **`bid_volumes`**
: `[10 + i % 5 for i in range(100)]`


- **`ask_volumes`**
: `[12 + i % 3 for i in range(100)]`


- **`mid_price`**
: `(pl.col('bid') + pl.col('ask')) / 2`


- **`enriched_tick_data`**
: `tick_data.with_columns(mid_open=mid_price, mid_high=mid_price, mid_low=mid_price, mid_close=mid_price, bid_open=pl.col('bid'), bid_high=pl.col('bid'), bid_low=pl.col('bid'), bid_close=pl.col('bid'), ask_open=pl.col('ask'), ask_high=pl.col('ask'), ask_low=pl.col('ask'), ask_close=pl.col('ask'), spread=pl.col('ask') - pl.col('bid'), real_volume=pl.col('bid_volume') + pl.col('ask_volume'), tick_volume=pl.lit(1))`


- **`result`**
: `enriched_tick_data`


- **`required_columns`**
: `['mid_close', 'spread', 'tick_volume']`


- **`missing_columns`**
: `[col for col in required_columns if col not in result.columns]`


- **`config_manager`**
: `YAMLConfigManager()`


- **`processor`**
: `D01PriceProcessor(config_manager, logger)`


- **`result`**
: `processor.process(resample_data, 'tick')`


- **`shadow_columns`**
: `['upper_shadow', 'lower_shadow']`


- **`original_columns`**
: `['timestamp', 'bid', 'ask', 'bid_volume', 'ask_volume']`


- **`missing_originals`**
: `[col for col in original_columns if col not in result.columns]`


- **`success`**
: `validate_tick_pipeline()`


## Osztály: `MockLogger`

### Metódusok

#### `info()`

```python
def info(self, message: str) -> None
```

**Paraméterek:**

- **`self`**
- **`message`** (`str`)

**Visszatérési érték:**

- Típus: `None`

#### `error()`

```python
def error(self, message: str) -> None
```

**Paraméterek:**

- **`self`**
- **`message`** (`str`)

**Visszatérési érték:**

- Típus: `None`

#### `debug()`

```python
def debug(self, message: str) -> None
```

**Paraméterek:**

- **`self`**
- **`message`** (`str`)

**Visszatérési érték:**

- Típus: `None`

#### `warning()`

```python
def warning(self, message: str) -> None
```

**Paraméterek:**

- **`self`**
- **`message`** (`str`)

**Visszatérési érték:**

- Típus: `None`

### `validate_tick_pipeline()`

```python
def validate_tick_pipeline() -> bool
```

Tick pipeline validáció végrehajtása.

**Visszatérési érték:**

- Típus: `bool`
- bool: True ha minden validáció sikeres, False egyébként

### `_create_mock_config()`

```python
def _create_mock_config() -> dict[str, Any]
```

Mock konfiguráció létrehozása.

**Visszatérési érték:**

- Típus: `dict[str, Any]`

### `_create_mock_logger()`

```python
def _create_mock_logger() -> Any
```

Mock logger objektum létrehozása.

**Visszatérési érték:**

- Típus: `Any`

### `_generate_test_tick_data()`

```python
def _generate_test_tick_data() -> pl.DataFrame
```

Mock tick adatok generálása teszteléshez.

**Visszatérési érték:**

- Típus: `pl.DataFrame`

### `_validate_resample()`

```python
def _validate_resample(tick_data: pl.DataFrame, logger: Any) -> pl.DataFrame | None
```

Resample komponens validációja.

**Paraméterek:**

- **`tick_data`** (`pl.DataFrame`): Bemeneti tick adatok
- **`logger`** (`Any`): Logger

**Visszatérési érték:**

- Típus: `pl.DataFrame | None`
- Resample eredmény vagy None ha hiba

### `_validate_d1_processor()`

```python
def _validate_d1_processor(resample_data: pl.DataFrame, config: dict[str, Any], logger: Any) -> bool
```

D1 Dimension Processor validációja.

**Paraméterek:**

- **`resample_data`** (`pl.DataFrame`): Resample eredmény
- **`config`** (`dict[str, Any]`): Konfiguráció
- **`logger`** (`Any`): Logger

**Visszatérési érték:**

- Típus: `bool`
- bool: True ha valid, False egyébként

### `main()`

```python
def main() -> int
```

Fő végrehajtási függvény.

**Visszatérési érték:**

- Típus: `int`
- int: Kilépési kód (0 = siker, 1 = hiba)

---

**Forrásfájl:** [`scripts/test_tick_pipeline.py`](../../scripts/test_tick_pipeline.py)
