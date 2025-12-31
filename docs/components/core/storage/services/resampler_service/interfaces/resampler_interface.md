# ResamplerInterface

## Áttekintés

A `ResamplerInterface` egy absztrakt interfész, amely definiálja a tick adatok OHLCV (Open, High, Low, Close, Volume) gyertyákká alakításának műveleteit. Ez az interfész biztosítja a standardizált átalakítási folyamatot a különböző időkeretekben.

## Osztály

```python
class ResamplerInterface(ABC)
```

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
) -> "DataFrame"
```

**Paraméterek:**

- `symbol` (str): A kereskedési szimbólum (pl. 'EURUSD')
- `start` (datetime): A kezdő időpont
- `end` (datetime): A záró időpont
- `timeframe` (str, opcionális): Az időkeret (alapértelmezett: '1m' - 1 perc)

**Visszatérési érték:**

- `DataFrame`: OHLCV gyertyákat tartalmazó DataFrame

**Kivételek:**

- `ResamplerError`: Ha hiba történik az átalakítás során

## Használati példa

```python
from datetime import datetime
from neural_ai.core.storage.services.resampler_service import ResamplerInterface

# Interfész használata
resampler: ResamplerInterface = ...

# Tick adatok átalakítása 5 perces gyertyákká
start = datetime(2024, 1, 1, 0, 0, 0)
end = datetime(2024, 1, 1, 23, 59, 59)
ohlcv_data = await resampler.resample(
    symbol="EURUSD",
    start=start,
    end=end,
    timeframe="5m"
)
```

## Implementációk

- [`ResamplerService`](../implementations/resampler_service.md): A fő implementáció Polars használatával

## Lásd még

- [ResamplerService](../implementations/resampler_service.md)
- [ResamplerServiceFactory](../factory.md)
- [ResamplerError](../exceptions/resampler_error.md)