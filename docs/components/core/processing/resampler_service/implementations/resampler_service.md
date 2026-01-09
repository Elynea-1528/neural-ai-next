# ResamplerService Implementáció

## Áttekintés

A `ResamplerService` a tick adatokat alakítja át OHLCV (Open, High, Low, Close, Volume) gyertyákká a megadott időkeretben. A szolgáltatás a Polars `group_by_dynamic` funkcióját használja a hatékony csoportosításhoz és aggregációhoz.

## Fő jellemzők

- **Tick adatok betöltése**: A `ParquetStorageService.read_tick_data` metódusán keresztül tölti be az adatokat
- **Gyors aggregáció**: Polars `group_by_dynamic` használata a Pandas `resample` helyett
- **Támogatott időkeretek**: 1m, 5m, 15m, 30m, 1h, 4h, 1D, 1W, 1M
- **Volume aggregáció**: Bid/Ask volume külön aggregálása

## Osztály struktúra

```python
class ResamplerService(ResamplerInterface):
    """Tick adatokból OHLCV gyertyák létrehozása."""
    
    def __init__(self, storage: "StorageInterface") -> None:
        """Inicializálás Storage interfésszel."""
        
    async def resample(
        self, symbol: str, start: datetime, end: datetime, timeframe: str = "1m"
    ) -> pd.DataFrame:
        """Tick adatok átalakítása OHLCV gyertyákká."""
```

## Metódusok

### `__init__(storage: StorageInterface)`

A konstruktor Dependency Injection-nel kapja meg a tárolási interfészt.

### `async resample(symbol, start, end, timeframe) -> pd.DataFrame`

A fő metódus, amely elvégzi a teljes átalakítást:

1. Validálja az időkeretet
2. Betölti a tick adatokat a storage-ból
3. Átalakítja OHLCV gyertyákká
4. Visszaadja a Pandas DataFrame-et

### `_load_tick_data(symbol, start, end) -> pl.DataFrame`

Betölti a tick adatokat a `ParquetStorageService.read_tick_data` metódusán keresztül.

### `_convert_to_ohlcv(tick_data, timeframe) -> pd.DataFrame`

A Polars `group_by_dynamic` használatával végzi el az aggregációt:

- **Open**: `price.first()` - az első ár a gyertyában
- **High**: `price.max()` - a maximum ár
- **Low**: `price.min()` - a minimum ár
- **Close**: `price.last()` - az utolsó ár
- **Volume**: `volume.sum()` - összes volumen

## Aggregáció specifikáció

```
Open = first(bid)
High = max(bid)
Low = min(bid)
Close = last(bid)
Volume = sum(volume)
Bid Volume = sum(bid_volume)
Ask Volume = sum(ask_volume)
```

## Használat példa

```python
from datetime import datetime
from neural_ai.core.processing.resampler_service.factory import ResamplerServiceFactory

# Factory-n keresztül példányosítás
resampler = ResamplerServiceFactory.get_resampler()

# OHLCV gyertyák létrehozása
start = datetime(2024, 1, 1)
end = datetime(2024, 1, 2)
ohlcv = await resampler.resample("EURUSD", start, end, timeframe="1m")

print(ohlcv.head())
```

## Függőségek

- `polars`: Gyors DataFrame műveletek és csoportosítás
- `pandas`: Visszatérési érték formátum
- `structlog`: Naplózás
- `ParquetStorageService`: Tick adatok betöltése

## Kivételek

- `InvalidTimeframeError`: Érvénytelen időkeret esetén
- `DataLoadError`: Hiba az adatbetöltés során
- `ResamplingError`: Hiba az átalakítás során
