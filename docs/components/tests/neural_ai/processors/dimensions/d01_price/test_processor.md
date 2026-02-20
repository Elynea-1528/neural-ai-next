# tests/neural_ai/processors/dimensions/d01_price/test_processor.py

Unit tesztek a D01PriceProcessor osztályhoz.

## Importok

```python
from unittest.mock import MagicMock
import polars
import pytest
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
from neural_ai.processors.dimensions.d01_price.processor import D01PriceProcessor
```

## Konstansok

- **`config`**
: `MagicMock(spec=ConfigManagerInterface)`


## Osztály: `TestD01PriceProcessorInitialization`

D01PriceProcessor inicializálás tesztjei.

### Metódusok

#### `test_init_success()`

```python
def test_init_success(self, mock_config: MagicMock, mock_logger: MagicMock) -> None
```

Sikeres inicializálás tesztje.

**Paraméterek:**

- **`self`**
- **`mock_config`** (`MagicMock`)
- **`mock_logger`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_dimension_id_property()`

```python
def test_dimension_id_property(self, mock_config: MagicMock, mock_logger: MagicMock) -> None
```

Dimenzió ID property tesztje.

**Paraméterek:**

- **`self`**
- **`mock_config`** (`MagicMock`)
- **`mock_logger`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestD01PriceProcessorProcess`

D01PriceProcessor process metódus tesztjei.

### Metódusok

#### `test_process_happy_path()`

```python
def test_process_happy_path(self, mock_config: MagicMock, mock_logger: MagicMock, sample_ohlcv_data: pl.DataFrame) -> None
```

Process metódus normál működés tesztje.

**Paraméterek:**

- **`self`**
- **`mock_config`** (`MagicMock`)
- **`mock_logger`** (`MagicMock`)
- **`sample_ohlcv_data`** (`pl.DataFrame`)

**Visszatérési érték:**

- Típus: `None`

#### `test_process_calculates_log_return()`

```python
def test_process_calculates_log_return(self, mock_config: MagicMock, mock_logger: MagicMock, sample_ohlcv_data: pl.DataFrame) -> None
```

Log return számítás tesztje.

**Paraméterek:**

- **`self`**
- **`mock_config`** (`MagicMock`)
- **`mock_logger`** (`MagicMock`)
- **`sample_ohlcv_data`** (`pl.DataFrame`)

**Visszatérési érték:**

- Típus: `None`

#### `test_process_calculates_bid_ask_from_spread()`

```python
def test_process_calculates_bid_ask_from_spread(self, mock_config: MagicMock, mock_logger: MagicMock, sample_ohlcv_data: pl.DataFrame) -> None
```

Bid/Ask számítás spread alapján tesztje.

**Paraméterek:**

- **`self`**
- **`mock_config`** (`MagicMock`)
- **`mock_logger`** (`MagicMock`)
- **`sample_ohlcv_data`** (`pl.DataFrame`)

**Visszatérési érték:**

- Típus: `None`

#### `test_process_calculates_shadows_for_ohlc()`

```python
def test_process_calculates_shadows_for_ohlc(self, mock_config: MagicMock, mock_logger: MagicMock, sample_ohlcv_data: pl.DataFrame) -> None
```

Árnyékok számítása OHLC timeframe esetén.

**Paraméterek:**

- **`self`**
- **`mock_config`** (`MagicMock`)
- **`mock_logger`** (`MagicMock`)
- **`sample_ohlcv_data`** (`pl.DataFrame`)

**Visszatérési érték:**

- Típus: `None`

#### `test_process_no_shadows_for_tick_timeframe()`

```python
def test_process_no_shadows_for_tick_timeframe(self, mock_config: MagicMock, mock_logger: MagicMock, sample_ohlcv_data: pl.DataFrame) -> None
```

Árnyékok NEM számítása tick timeframe esetén.

**Paraméterek:**

- **`self`**
- **`mock_config`** (`MagicMock`)
- **`mock_logger`** (`MagicMock`)
- **`sample_ohlcv_data`** (`pl.DataFrame`)

**Visszatérési érték:**

- Típus: `None`

#### `test_process_with_custom_z_score_window()`

```python
def test_process_with_custom_z_score_window(self, mock_config: MagicMock, mock_logger: MagicMock, sample_ohlcv_data: pl.DataFrame) -> None
```

Egyedi Z-score ablak használata.

**Paraméterek:**

- **`self`**
- **`mock_config`** (`MagicMock`)
- **`mock_logger`** (`MagicMock`)
- **`sample_ohlcv_data`** (`pl.DataFrame`)

**Visszatérési érték:**

- Típus: `None`

#### `test_process_with_timeframe_specific_config()`

```python
def test_process_with_timeframe_specific_config(self, mock_config: MagicMock, mock_logger: MagicMock, sample_ohlcv_data: pl.DataFrame) -> None
```

Timeframe specifikus konfiguráció használata.

**Paraméterek:**

- **`self`**
- **`mock_config`** (`MagicMock`)
- **`mock_logger`** (`MagicMock`)
- **`sample_ohlcv_data`** (`pl.DataFrame`)

**Visszatérési érték:**

- Típus: `None`

#### `test_process_preserves_existing_bid_ask_columns()`

```python
def test_process_preserves_existing_bid_ask_columns(self, mock_config: MagicMock, mock_logger: MagicMock) -> None
```

Meglévő bid/ask oszlopok megőrzése.

**Paraméterek:**

- **`self`**
- **`mock_config`** (`MagicMock`)
- **`mock_logger`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestD01PriceProcessorEdgeCases`

D01PriceProcessor edge case tesztek.

### Metódusok

#### `test_process_with_empty_dataframe()`

```python
def test_process_with_empty_dataframe(self, mock_config: MagicMock, mock_logger: MagicMock) -> None
```

Üres DataFrame kezelése.

**Paraméterek:**

- **`self`**
- **`mock_config`** (`MagicMock`)
- **`mock_logger`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_process_with_single_row()`

```python
def test_process_with_single_row(self, mock_config: MagicMock, mock_logger: MagicMock) -> None
```

Egyetlen sor kezelése.

**Paraméterek:**

- **`self`**
- **`mock_config`** (`MagicMock`)
- **`mock_logger`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_process_with_calc_shadows_disabled()`

```python
def test_process_with_calc_shadows_disabled(self, mock_config: MagicMock, mock_logger: MagicMock, sample_ohlcv_data: pl.DataFrame) -> None
```

Árnyék számítás kikapcsolva.

**Paraméterek:**

- **`self`**
- **`mock_config`** (`MagicMock`)
- **`mock_logger`** (`MagicMock`)
- **`sample_ohlcv_data`** (`pl.DataFrame`)

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestD01PriceProcessorMarketHours`

D01PriceProcessor market hours szűrés tesztjei.

### Metódusok

#### `test_process_with_market_hours_disabled()`

```python
def test_process_with_market_hours_disabled(self, mock_config: MagicMock, mock_logger: MagicMock, sample_ohlcv_data: pl.DataFrame) -> None
```

Market hours szűrés kikapcsolva.

**Paraméterek:**

- **`self`**
- **`mock_config`** (`MagicMock`)
- **`mock_logger`** (`MagicMock`)
- **`sample_ohlcv_data`** (`pl.DataFrame`)

**Visszatérési érték:**

- Típus: `None`

#### `test_process_with_market_hours_enabled_no_filtering()`

```python
def test_process_with_market_hours_enabled_no_filtering(self, mock_config: MagicMock, mock_logger: MagicMock, sample_ohlcv_data: pl.DataFrame) -> None
```

Market hours szűrés bekapcsolva, de nincs szűrés (minden adat market hours-ban).

**Paraméterek:**

- **`self`**
- **`mock_config`** (`MagicMock`)
- **`mock_logger`** (`MagicMock`)
- **`sample_ohlcv_data`** (`pl.DataFrame`)

**Visszatérési érték:**

- Típus: `None`

#### `test_process_with_market_hours_logging_triggered()`

```python
def test_process_with_market_hours_logging_triggered(self, mock_config: MagicMock, mock_logger: MagicMock) -> None
```

Market hours szűrés logging aktiválása hétvégi adatokkal.

**Paraméterek:**

- **`self`**
- **`mock_config`** (`MagicMock`)
- **`mock_logger`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestD01PriceProcessorTickColumns`

D01PriceProcessor tick oszlopok kezelése tesztjei.

### Metódusok

#### `test_process_with_tick_columns()`

```python
def test_process_with_tick_columns(self, mock_config: MagicMock, mock_logger: MagicMock) -> None
```

Tick oszlopok hozzáadása, ha rendelkezésre állnak.

**Paraméterek:**

- **`self`**
- **`mock_config`** (`MagicMock`)
- **`mock_logger`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_process_without_tick_columns()`

```python
def test_process_without_tick_columns(self, mock_config: MagicMock, mock_logger: MagicMock, sample_ohlcv_data: pl.DataFrame) -> None
```

Tick oszlopok hiánya nem okoz hibát.

**Paraméterek:**

- **`self`**
- **`mock_config`** (`MagicMock`)
- **`mock_logger`** (`MagicMock`)
- **`sample_ohlcv_data`** (`pl.DataFrame`)

**Visszatérési érték:**

- Típus: `None`

### `mock_config()`

```python
def mock_config() -> MagicMock
```

Mock ConfigManagerInterface fixture.

**Visszatérési érték:**

- Típus: `MagicMock`

### `mock_logger()`

```python
def mock_logger() -> MagicMock
```

Mock LoggerInterface fixture.

**Visszatérési érték:**

- Típus: `MagicMock`

### `sample_ohlcv_data()`

```python
def sample_ohlcv_data() -> pl.DataFrame
```

Minta OHLCV adat fixture.

**Visszatérési érték:**

- Típus: `pl.DataFrame`

---

**Forrásfájl:** [`tests/neural_ai/processors/dimensions/d01_price/test_processor.py`](../../tests/neural_ai/processors/dimensions/d01_price/test_processor.py)
