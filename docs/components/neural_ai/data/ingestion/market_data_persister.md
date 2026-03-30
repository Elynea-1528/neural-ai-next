# neural_ai/data/ingestion/market_data_persister.py

MarketDataPersister szolgáltatás.

Ez a modul implementálja a MarketDataPersister osztályt, amely felelős
a bejövő market data eventek bufferezéséért és időzített mentéséért
a Parquet tárolóba.

Author: Neural AI Next Team
Version: 1.0.0

## Importok

```python
import asyncio
from collections import defaultdict
from datetime import UTC
from datetime import datetime
from typing import TYPE_CHECKING
from typing import Any
from typing import Union
from typing import cast
from neural_ai.core.config.interfaces.types import IngestionConfig
from neural_ai.core.events.interfaces.event_models import MarketDataEvent
# ... és még 14 import
```

## Osztály: `MarketDataPersister`

Market data eventeket bufferez és menti a tárolóba.

Ez az osztály felelős azért, hogy a bejövő market data eventeket
gyűjtse egy belső bufferbe, és amikor a buffer eléri a méretkorlátot
vagy új óra kezdődik, akkor a buffert kiürítse és elmentse a
Parquet tárolóba.

Attributes:
    event_bus: Az EventBus interfész példánya
    storage: A Storage interfész példánya
    logger: A Logger interfész példánya
    buffer: A tick adatok buffere szimbólumonként csoportosítva
    buffer_size_limit: A buffer méretkorlátja (alapértelmezett: 10.000 tick)
    current_hour: Az aktuális óra az időzített flush-hoz
    running: A szolgáltatás futásállapota

### Metódusok

#### `__init__()`

```python
def __init__(self, event_bus: 'EventBusInterface', storage: 'StorageInterface', logger: 'LoggerInterface', config: IngestionConfig) -> None
```

Inicializálja a MarketDataPersister-t.

**Paraméterek:**

- **`self`**
- **`event_bus`** (`'EventBusInterface'`): Az EventBus interfész példánya
- **`storage`** (`'StorageInterface'`): A Storage interfész példánya
- **`logger`** (`'LoggerInterface'`): A Logger interfész példánya
- **`config`** (`IngestionConfig`): Az ingestion konfiguráció

**Visszatérési érték:**

- Típus: `None`

#### `start()`

```python
async def start(self) -> None
```

Elindítja a MarketDataPersister szolgáltatást. Feliratkozás a market_data topicra és elindítja a háttérfeladatot az időzített flush-hoz.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `stop()`

```python
async def stop(self) -> None
```

Leállítja a MarketDataPersister szolgáltatást. Kiüríti a maradék buffert és leiratkozik az eventekről.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `on_market_data()`

```python
async def on_market_data(self, event: MarketDataEvent | list[MarketDataEvent]) -> None
```

Fogadja a market data eventeket (vagy batch listát) és bufferezi őket.

**Paraméterek:**

- **`self`**
- **`event`** (`MarketDataEvent | list[MarketDataEvent]`): Egy MarketDataEvent VAGY MarketDataEvent-ek listája.

**Visszatérési érték:**

- Típus: `None`

#### `_periodic_flush_task()`

```python
async def _periodic_flush_task(self) -> None
```

Háttérfeladat az időzített buffer kiürítéshez. Minden órában ellenőrzi, hogy új óra kezdődött-e, és ha igen, kiüríti a buffert.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `_flush_all_buffers()`

```python
async def _flush_all_buffers(self) -> None
```

Kiüríti az összes buffert és elmenti a tárolóba. Szimbólumonként csoportosítva konvertálja DataFrame-é és menti.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `_flush_symbol_buffer()`

```python
async def _flush_symbol_buffer(self, symbol: str, events: list[MarketDataEvent]) -> None
```

Kiüríti egy adott szimbólum bufferét.

**Paraméterek:**

- **`self`**
- **`symbol`** (`str`): A szimbólum neve
- **`events`** (`list[MarketDataEvent]`): A kiürítendő eventek listája

**Visszatérési érték:**

- Típus: `None`

#### `_save_events_to_storage()`

```python
async def _save_events_to_storage(self, symbol: str, events: list[MarketDataEvent], date: datetime) -> None
```

Elmenti az eventeket a tárolóba.

**Paraméterek:**

- **`self`**
- **`symbol`** (`str`): A szimbólum neve
- **`events`** (`list[MarketDataEvent]`): Az elmentendő eventek listája
- **`date`** (`datetime`): A dátum, ami alapján a particionálás történik

**Visszatérési érték:**

- Típus: `None`

#### `_convert_events_to_dataframe()`

```python
def _convert_events_to_dataframe(self, events: list[MarketDataEvent]) -> Union['pl.DataFrame', 'pd.DataFrame']
```

Konvertálja az eventeket DataFrame-é.

**Paraméterek:**

- **`self`**
- **`events`** (`list[MarketDataEvent]`): A konvertálandó eventek listája

**Visszatérési érték:**

- Típus: `Union['pl.DataFrame', 'pd.DataFrame']`
- A konvertált DataFrame

---

**Forrásfájl:** [`neural_ai/data/ingestion/market_data_persister.py`](../../neural_ai/data/ingestion/market_data_persister.py)
