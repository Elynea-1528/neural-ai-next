# tests/neural_ai/data/ingestion/test_market_data_persister.py

Tesztek a MarketDataPersister szolgáltatáshoz.

Ez a modul tartalmazza a MarketDataPersister osztály átfogó tesztjeit,
amelyek ellenőrzik a market data eventek bufferezését és mentését.

## Importok

```python
import asyncio
from contextlib import suppress
from datetime import UTC
from datetime import datetime
from datetime import timedelta
from typing import cast
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch
import pytest
# ... és még 4 import
```

## Osztály: `MockMarketDataEvent(BaseModel)`

Mock market data event a teszteléshez.

## Osztály: `TestMarketDataPersisterInit`

Tesztek a MarketDataPersister inicializálásához.

### Metódusok

#### `test_init_with_default_values()`

```python
def test_init_with_default_values(self) -> None
```

Teszteli az alapértelmezett értékekkel történő inicializálást.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_init_with_custom_buffer_size()`

```python
def test_init_with_custom_buffer_size(self) -> None
```

Teszteli az egyéni buffer mérettel történő inicializálást.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestMarketDataPersisterStartStop`

Tesztek a MarketDataPersister indításához és leállításához.

### Metódusok

#### `test_start_success()`

```python
async def test_start_success(self) -> None
```

Teszteli a sikeres indítást.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_start_when_already_running()`

```python
async def test_start_when_already_running(self) -> None
```

Teszteli az indítást, ha már fut a szolgáltatás.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_stop_success()`

```python
async def test_stop_success(self) -> None
```

Teszteli a sikeres leállítást.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_stop_when_not_running()`

```python
async def test_stop_when_not_running(self) -> None
```

Teszteli a leállítást, ha nem fut a szolgáltatás.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestMarketDataPersisterOnMarketData`

Tesztek az on_market_data eseménykezelőhöz.

### Metódusok

#### `test_on_market_data_single_event()`

```python
async def test_on_market_data_single_event(self) -> None
```

Teszteli egyetlen event fogadását.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_on_market_data_batch_events()`

```python
async def test_on_market_data_batch_events(self) -> None
```

Teszteli batch eventek fogadását.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_on_market_data_unknown_format()`

```python
async def test_on_market_data_unknown_format(self) -> None
```

Teszteli ismeretlen formátumú event kezelését.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_on_market_data_triggers_flush_at_limit()`

```python
async def test_on_market_data_triggers_flush_at_limit(self) -> None
```

Teszteli, hogy a buffer kiürül, ha eléri a méretkorlátot.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestMarketDataPersisterPeriodicFlush`

Tesztek a periodikus flush taskhoz.

### Metódusok

#### `test_periodic_flush_triggers_on_new_hour()`

```python
async def test_periodic_flush_triggers_on_new_hour(self) -> None
```

Teszteli, hogy az új óra kezdetekor lefut-e a flush.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_periodic_flush_handles_exception()`

```python
async def test_periodic_flush_handles_exception(self) -> None
```

Teszteli a kivétel kezelését a periodikus flush során.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestMarketDataPersisterFlush`

Tesztek a buffer kiürítéshez.

### Metódusok

#### `test_flush_all_buffers_with_data()`

```python
async def test_flush_all_buffers_with_data(self) -> None
```

Teszteli az összes buffer kiürítését adatokkal.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_flush_all_buffers_empty()`

```python
async def test_flush_all_buffers_empty(self) -> None
```

Teszteli az üres buffer kiürítését.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_flush_symbol_buffer_success()`

```python
async def test_flush_symbol_buffer_success(self) -> None
```

Teszteli egy szimbólum bufferének sikeres kiürítését.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_flush_symbol_buffer_empty()`

```python
async def test_flush_symbol_buffer_empty(self) -> None
```

Teszteli az üres szimbólum buffer kiürítését.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_flush_symbol_buffer_handles_exception()`

```python
async def test_flush_symbol_buffer_handles_exception(self) -> None
```

Teszteli a kivétel kezelését a szimbólum buffer kiürítésekor.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestMarketDataPersisterSave`

Tesztek az adatok tárolóba mentéséhez.

### Metódusok

#### `test_save_events_to_storage_with_parquet_service()`

```python
async def test_save_events_to_storage_with_parquet_service(self) -> None
```

Teszteli az eventek mentését ParquetStorageService használatával.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_save_events_to_storage_fallback()`

```python
async def test_save_events_to_storage_fallback(self) -> None
```

Teszteli az eventek mentését fallback metódussal.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_save_events_to_storage_empty()`

```python
async def test_save_events_to_storage_empty(self) -> None
```

Teszteli az üres event lista mentését.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_save_events_to_storage_handles_exception()`

```python
async def test_save_events_to_storage_handles_exception(self) -> None
```

Teszteli a kivétel kezelését az eventek mentésekor.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestMarketDataPersisterConvertToDataFrame`

Tesztek a DataFrame konverzióhoz.

### Metódusok

#### `test_convert_events_to_dataframe_with_pandas()`

```python
def test_convert_events_to_dataframe_with_pandas(self) -> None
```

Teszteli az eventek DataFrame-é konvertálását pandas használatával.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_convert_events_to_dataframe_with_polars()`

```python
def test_convert_events_to_dataframe_with_polars(self) -> None
```

Teszteli az eventek DataFrame-é konvertálását polars használatával.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_convert_events_to_dataframe_no_library()`

```python
def test_convert_events_to_dataframe_no_library(self) -> None
```

Teszteli a kivételt, ha egyik library sincs telepítve.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestMarketDataPersisterIntegration`

Integrációs tesztek a MarketDataPersister-hez.

### Metódusok

#### `test_full_workflow()`

```python
async def test_full_workflow(self) -> None
```

Teszteli a teljes munkafolyamatot.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/data/ingestion/test_market_data_persister.py`](../../tests/neural_ai/data/ingestion/test_market_data_persister.py)
