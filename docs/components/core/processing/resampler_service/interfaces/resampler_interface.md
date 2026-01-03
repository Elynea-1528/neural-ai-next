# ResamplerInterface

## Áttekintés

A `ResamplerInterface` egy absztrakt interfész, amely definiálja a tick adatok OHLCV gyertyákká alakításához szükséges metódusokat. Ez az interfész biztosítja a konzisztenciát a ResamplerService különböző implementációi között.

## Interfész definíció

```python
from abc import ABC, abstractmethod
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pandas import DataFrame


class ResamplerInterface(ABC):
    """ResamplerService interfész, amely definiálja a tick adatok OHLCV gyertyákká alakítását."""
    
    @abstractmethod
    async def resample(
        self,
        symbol: str,
        start: datetime,
        end: datetime,
        timeframe: str = '1m'
    ) -> "DataFrame":
        """Tick adatok átalakítása OHLCV gyertyákká a megadott időkeretben."""
        pass
```

## Metódusok

### `resample(symbol, start, end, timeframe)`

Aszinkron absztrakt metódus, amely tick adatokat alakít át OHLCV gyertyákká.

**Paraméterek:**

| Paraméter | Típus | Leírás | Alapértelmezett |
|-----------|-------|---------|-----------------|
| `symbol` | `str` | A kereskedési szimbólum (pl. 'EURUSD') | Kötelező |
| `start` | `datetime` | A kezdő időpont | Kötelező |
| `end` | `datetime` | A záró időpont | Kötelező |
| `timeframe` | `str` | Az időkeret | '1m' |

**Visszatérési érték:**
- `DataFrame`: OHLCV gyertyákat tartalmazó Pandas DataFrame

**Kivételek:**
- `ResamplerError`: Ha hiba történik az átalakítás során
- `InvalidTimeframeError`: Ha az időkeret érvénytelen
- `DataLoadError`: Ha hiba történik az adatok betöltése során

## Támogatott időkeretek

A következő időkeretek támogatottak:

| Időkeret | Leírás |
|----------|---------|
| `1m` | 1 perc |
| `5m` | 5 perc |
| `15m` | 15 perc |
| `30m` | 30 perc |
| `1h` | 1 óra |
| `4h` | 4 óra |
| `1D` | 1 nap |
| `1W` | 1 hét |
| `1M` | 1 hónap |

## Implementáció követelmények

Minden `ResamplerInterface` implementációnak kötelezően implementálnia kell:

1. **Aszinkron művelet**: A `resample` metódusnak aszinkronnak kell lennie
2. **Időkeret validáció**: Ellenőriznie kell az időkeret érvényességét
3. **Hibatűrés**: Hibák esetén részletes információt kell szolgáltatnia
4. **Típuskonzisztencia**: A visszaadott DataFrame-nek tartalmaznia kell az OHLCV oszlopokat

## Várt kimenet formátum

A metódus egy Pandas DataFrame-et ad vissza a következő struktúrával:

```python
import pandas as pd

# Várt DataFrame struktúra
df = pd.DataFrame({
    'open': [1.0850, 1.0852, ...],
    'high': [1.0855, 1.0858, ...],
    'low': [1.0848, 1.0850, ...],
    'close': [1.0852, 1.0855, ...],
    'volume': [1000, 1200, ...]
}, index=pd.DatetimeIndex([
    '2024-01-01 00:00:00',
    '2024-01-01 00:01:00',
    ...
]))
```

## Példa implementáció

```python
from neural_ai.core.processing.resampler_service.interfaces.resampler_interface import (
    ResamplerInterface,
)
from neural_ai.core.storage.interfaces.storage_interface import StorageInterface


class CustomResampler(ResamplerInterface):
    """Egyéni Resampler implementáció."""
    
    def __init__(self, storage: StorageInterface):
        self._storage = storage
    
    async def resample(
        self,
        symbol: str,
        start: datetime,
        end: datetime,
        timeframe: str = '1m'
    ) -> "DataFrame":
        """Implementáció."""
        # Egyéni logika
        pass
```

## Hibakezelés

Az interfész definiálja a hibakezelés szabványait:

```python
from neural_ai.core.processing.resampler_service.exceptions.resampler_error import (
    DataLoadError,
    InvalidTimeframeError,
    ResamplingError,
)

# Példa hibakezelésre
try:
    result = await resampler.resample(symbol, start, end, timeframe)
except InvalidTimeframeError:
    # Érvénytelen időkeret
    pass
except DataLoadError:
    # Adatbetöltési hiba
    pass
except ResamplingError:
    # Átalakítási hiba
    pass
```

## Teljesítmény követelmények

Az interfész implicit követelményei:

1. **Aszinkron műveletek**: Nem blokkolhatja a fő szálat
2. **Memóriahatékonyság**: Nagy adatmennyiségek esetén is hatékonyan kell működnie
3. **Gyorsaság**: A resampling műveletnek gyorsnak kell lennie
4. **Skálázhatóság**: Több szimbólum és időkeret egyidejű kezelésére alkalmasnak kell lennie

## Kapcsolódó dokumentáció

- [ResamplerService](../index.md)
- [ResamplerService Implementation](../implementations/resampler_service.md)
- [ResamplerService Factory](../factory.md)
- [ResamplerService Exceptions](../exceptions/resampler_error.md)