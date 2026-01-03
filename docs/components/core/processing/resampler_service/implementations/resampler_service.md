# ResamplerService Implementáció

## Áttekintés

A `ResamplerService` a `ResamplerInterface` konkrét implementációja, amely tick adatokból hoz létre OHLCV (Open, High, Low, Close, Volume) gyertyákat a megadott időkeretekben. A hatékonyság érdekében Polars-t használ a nagy teljesítményű adatfeldolgozáshoz.

## Osztály struktúra

```python
class ResamplerService(ResamplerInterface):
    """ResamplerService implementáció, amely tick adatokból hoz létre OHLCV gyertyákat."""
    
    def __init__(self, storage: "StorageInterface") -> None:
        """ResamplerService inicializálása."""
        self._storage = storage
    
    async def resample(
        self,
        symbol: str,
        start: datetime,
        end: datetime,
        timeframe: str = '1m'
    ) -> pd.DataFrame:
        """Tick adatok átalakítása OHLCV gyertyákká."""
        pass
    
    def _validate_timeframe(self, timeframe: str) -> None:
        """Időkeret validálása."""
        pass
    
    async def _load_tick_data(
        self,
        symbol: str,
        start: datetime,
        end: datetime
    ) -> pl.DataFrame:
        """Tick adatok betöltése a tárolóból."""
        pass
    
    def _convert_to_ohlcv(
        self,
        tick_data: pl.DataFrame,
        timeframe: str
    ) -> pd.DataFrame:
        """Tick adatok átalakítása OHLCV gyertyákká."""
        pass
```

## Inicializálás

### Konstruktor

```python
def __init__(self, storage: "StorageInterface") -> None:
    """ResamplerService inicializálása.

    Args:
        storage: A tárolási interfész példány (Dependency Injection)
    """
    self._storage = storage
```

**Paraméterek:**
- `storage` (StorageInterface): A tárolási interfész példány

**Példa:**
```python
from neural_ai.core.storage.factory import StorageFactory
from neural_ai.core.processing.resampler_service.implementations.resampler_service import (
    ResamplerService,
)

storage = StorageFactory.get_storage(storage_type="parquet")
resampler = ResamplerService(storage=storage)
```

## Fő metódus: `resample()`

### Leírás

Az `resample()` metódus végzi el a tick adatok OHLCV gyertyákká alakítását.

### Paraméterek

| Paraméter | Típus | Leírás | Alapértelmezett |
|-----------|-------|---------|-----------------|
| `symbol` | `str` | A kereskedési szimbólum | Kötelező |
| `start` | `datetime` | Kezdő időpont | Kötelező |
| `end` | `datetime` | Záró időpont | Kötelező |
| `timeframe` | `str` | Időkeret | '1m' |

### Visszatérési érték

- `pd.DataFrame`: OHLCV gyertyákat tartalmazó DataFrame

### Kivételek

- `InvalidTimeframeError`: Ha az időkeret érvénytelen
- `DataLoadError`: Ha hiba történik az adatok betöltése során
- `ResamplingError`: Ha hiba történik az átalakítás során

### Implementáció folyamata

1. **Validáció**: Időkeret ellenőrzése
2. **Betöltés**: Tick adatok betöltése a tárolóból
3. **Átalakítás**: Tick → OHLCV konverzió
4. **Visszaadás**: Pandas DataFrame formátumban

### Példa

```python
from datetime import datetime

result = await resampler.resample(
    symbol="EURUSD",
    start=datetime(2024, 1, 1),
    end=datetime(2024, 1, 31),
    timeframe="1h"
)
```

## Segédmetódusok

### `_validate_timeframe(timeframe)`

Belső metódus az időkeret validálásához.

```python
def _validate_timeframe(self, timeframe: str) -> None:
    """Időkeret validálása.
    
    Args:
        timeframe: Az időkeret string
    
    Raises:
        InvalidTimeframeError: Ha az időkeret érvénytelen
    """
    valid_timeframes = ['1m', '5m', '15m', '30m', '1h', '4h', '1D', '1W', '1M']
    if timeframe not in valid_timeframes:
        raise InvalidTimeframeError(timeframe)
```

### `_load_tick_data(symbol, start, end)`

Aszinkron belső metódus a tick adatok betöltéséhez.

```python
async def _load_tick_data(
    self,
    symbol: str,
    start: datetime,
    end: datetime
) -> pl.DataFrame:
    """Tick adatok betöltése a tárolóból.
    
    Args:
        symbol: A kereskedési szimbólum
        start: A kezdő időpont
        end: A záró időpont
    
    Returns:
        Polars DataFrame a tick adatokkal
    
    Raises:
        DataLoadError: Ha hiba történik a betöltés során
    """
```

**Megjegyzés**: Ez egy ideiglenes implementáció. A valós implementációban a StorageInterface-en keresztül kell betölteni az adatokat.

### `_convert_to_ohlcv(tick_data, timeframe)`

Belső metódus a tick adatok OHLCV gyertyákká alakításához.

```python
def _convert_to_ohlcv(
    self,
    tick_data: pl.DataFrame,
    timeframe: str
) -> pd.DataFrame:
    """Tick adatok átalakítása OHLCV gyertyákká.
    
    Args:
        tick_data: Polars DataFrame tick adatokkal
        timeframe: Az időkeret
    
    Returns:
        Pandas DataFrame OHLCV gyertyákkal
    """
```

## OHLCV számítás részletei

### Ár számítás

```python
# Átlagár számítása (bid és ask átlaga)
tick_data = tick_data.with_columns(
    price=(pl.col("bid") + pl.col("ask")) / 2
)
```

### Aggregáció

```python
# OHLCV aggregáció Polars group_by_dynamic használatával
ohlcv = tick_data.group_by_dynamic(
    "timestamp",
    every=timeframe,
    period=timeframe
).agg([
    pl.col("price").first().alias("open"),
    pl.col("price").max().alias("high"),
    pl.col("price").min().alias("low"),
    pl.col("price").last().alias("close"),
    pl.col("volume").sum().alias("volume")
])
```

### Konverzió

```python
# Polars DataFrame konvertálása Pandas DataFrame-re
ohlcv_pandas = ohlcv.to_pandas()

# Index beállítása timestamp-re
ohlcv_pandas.set_index("timestamp", inplace=True)
```

## Teljesítmény optimalizációk

### 1. Polars használata

- **Gyorsaság**: Polars Rust-ban íródott, ezért sokkal gyorsabb, mint a Pandas
- **Memóriahatékonyság**: Hatékonyabb memóriakezelés
- **Parallel feldolgozás**: Automatikus párhuzamosítás

### 2. Group By Dynamic

```python
# Optimalizált aggregáció
ohlcv = tick_data.group_by_dynamic(
    "timestamp",
    every=timeframe,
    period=timeframe
).agg(...)
```

### 3. Lazy Evaluation

A Polars lazy evaluation-t használ, ami optimalizálja a számításokat.

## Adatfolyam diagram

```
┌─────────────────┐
│   Input: Tick   │
│   - symbol      │
│   - start       │
│   - end         │
│   - timeframe   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 1. Validáció    │
│    - timeframe  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 2. Betöltés     │
│    - tick data  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 3. Átalakítás   │
│    - OHLCV      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Output: OHLCV   │
│ DataFrame       │
└─────────────────┘
```

## Hibakezelés

### DataLoadError

```python
try:
    tick_data = await self._load_tick_data(symbol, start, end)
except DataLoadError:
    raise
except Exception as e:
    raise DataLoadError(
        symbol=symbol,
        start=str(start),
        end=str(end),
        original_error=e
    ) from e
```

### ResamplingError

```python
try:
    ohlcv_data = self._convert_to_ohlcv(tick_data, timeframe)
    return ohlcv_data
except Exception as e:
    raise ResamplingError(
        symbol=symbol,
        timeframe=timeframe,
        original_error=e
    ) from e
```

## Függőségek

- `pandas`: DataFrame kezelés
- `polars`: Nagy teljesítményű adatfeldolgozás
- `numpy`: Numerikus műveletek
- `neural_ai.core.storage`: Adattárolási réteg

## Jövőbeli fejlesztések

- [ ] Valós adatbetöltés a StorageInterface-en keresztül
- [ ] Több adatforrás támogatása
- [ ] Egyéni aggregációs függvények
- [ ] Real-time resampling
- [ ] Gyorsítótár-rendszer

## Kapcsolódó dokumentáció

- [ResamplerService](../index.md)
- [ResamplerInterface](../interfaces/resampler_interface.md)
- [ResamplerService Factory](../factory.md)
- [ResamplerService Exceptions](../exceptions/resampler_error.md)