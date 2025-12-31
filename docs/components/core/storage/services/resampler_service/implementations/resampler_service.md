# ResamplerService

## Áttekintés

A `ResamplerService` a [`ResamplerInterface`](../interfaces/resampler_interface.md) fő implementációja, amely tick adatokból hoz létre OHLCV (Open, High, Low, Close, Volume) gyertyákat. A hatékonyság érdekében Polars-t használ a nagy teljesítményű adatfeldolgozáshoz.

## Osztály

```python
class ResamplerService(ResamplerInterface)
```

## Konstruktor

```python
def __init__(self, storage: StorageInterface) -> None
```

**Paraméterek:**

- `storage` (StorageInterface): A tárolási interfész példány (Dependency Injection)

## Metódusok

### `resample()`

Tick adatok átalakítása OHLCV gyertyákká a megadott időkeretben.

```python
async def resample(
    self,
    symbol: str,
    start: datetime,
    end: datetime,
    timeframe: str = '1m'
) -> pd.DataFrame
```

**Paraméterek:**

- `symbol` (str): A kereskedési szimbólum (pl. 'EURUSD')
- `start` (datetime): A kezdő időpont
- `end` (datetime): A záró időpont
- `timeframe` (str, opcionális): Az időkeret (alapértelmezett: '1m')

**Visszatérési érték:**

- `pd.DataFrame`: OHLCV gyertyákat tartalmazó DataFrame

**Kivételek:**

- `InvalidTimeframeError`: Ha az időkeret érvénytelen
- `DataLoadError`: Ha hiba történik az adatok betöltése során
- `ResamplingError`: Ha hiba történik az átalakítás során

## Belső metódusok

### `_validate_timeframe()`

Időkeret validálása.

```python
def _validate_timeframe(self, timeframe: str) -> None
```

### `_load_tick_data()`

Tick adatok betöltése a tárolóból.

```python
async def _load_tick_data(
    self,
    symbol: str,
    start: datetime,
    end: datetime
) -> pl.DataFrame
```

### `_convert_to_ohlcv()`

Tick adatok átalakítása OHLCV gyertyákká Polars segítségével.

```python
def _convert_to_ohlcv(
    self,
    tick_data: pl.DataFrame,
    timeframe: str
) -> pd.DataFrame
```

## Támogatott időkeretek

- `1m` - 1 perc
- `5m` - 5 perc
- `15m` - 15 perc
- `30m` - 30 perc
- `1h` - 1 óra
- `4h` - 4 óra
- `1D` - 1 nap
- `1W` - 1 hét
- `1M` - 1 hónap

## Használati példa

```python
from datetime import datetime
from neural_ai.core.storage.services.resampler_service import (
    ResamplerServiceFactory,
    ResamplerInterface
)

# ResamplerService példány létrehozása
resampler: ResamplerInterface = ResamplerServiceFactory.get_instance()

# Tick adatok átalakítása 1 perces gyertyákká
start = datetime(2024, 1, 1, 0, 0, 0)
end = datetime(2024, 1, 1, 23, 59, 59)

try:
    ohlcv_data = await resampler.resample(
        symbol="EURUSD",
        start=start,
        end=end,
        timeframe="1m"
    )
    print(f"Létrejött {len(ohlcv_data)} gyertya")
except Exception as e:
    print(f"Hiba történt: {e}")
```

## Technológiai részletek

### Polars használata

A szolgáltatás Polars-t használ a nagy teljesítményű adatfeldolgozáshoz:

- `group_by_dynamic()`: Dinamikus csoportosítás időalapú ablakokban
- Hatékony aggregáció: `first()`, `max()`, `min()`, `last()`, `sum()`
- Memóriahatékony feldolgozás nagy adatmennyiségekhez

### OHLCV számítás

1. **Átlagár számítása**: `price = (bid + ask) / 2`
2. **Időalapú csoportosítás**: A megadott `timeframe` szerint
3. **Aggregáció**:
   - Open: Az első ár az időkeretben
   - High: A legmagasabb ár az időkeretben
   - Low: A legalacsonyabb ár az időkeretben
   - Close: Az utolsó ár az időkeretben
   - Volume: A volumenek összege az időkeretben

## Lásd még

- [ResamplerInterface](../interfaces/resampler_interface.md)
- [ResamplerServiceFactory](../factory.md)
- [ResamplerError](../exceptions/resampler_error.md)