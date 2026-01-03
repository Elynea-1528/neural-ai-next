# ResamplerService

## Áttekintés

A `ResamplerService` a `neural_ai.core.processing` modul kulcsfontosságú komponense, amely tick adatokból OHLCV (Open, High, Low, Close, Volume) gyertyákat generál a megadott időkeretekben. Ez a szolgáltatás kritikus fontosságú a technikai elemzéshez és a kereskedési stratégiák fejlesztéséhez.

## Architektúra

A ResamplerService szigorúan követi a rendszer architektúra szabványait:

```
neural_ai/core/processing/resampler_service/
├── interfaces/
│   └── resampler_interface.py      # Az interfész definíciója
├── implementations/
│   └── resampler_service.py        # A konkrét implementáció
├── exceptions/
│   └── resampler_error.py          # Egyéni kivételek
├── factory.py                      # Factory osztály
└── __init__.py                     # Modul inicializálás
```

## Főbb jellemzők

### 1. Időkeret-támogatás

A szolgáltatás a következő időkereteket támogatja:
- **Perces**: 1m, 5m, 15m, 30m
- **Órás**: 1h, 4h
- **Napi**: 1D
- **Heti**: 1W
- **Havi**: 1M

### 2. Teljesítmény-optimalizálás

- **Polars használata**: A nagy teljesítményű Polars könyvtárat használja az adatfeldolgozáshoz
- **Aszinkron műveletek**: Az összes művelet aszinkron, nem blokkolja a fő szálat
- **Memóriahatékony**: Chunk-based feldolgozás nagy adatmennyiségekhez

### 3. Hibatűrés

- **Resilient design**: Hibák esetén részletes információt szolgáltat
- **Validáció**: Időkeret-validáció a feldolgozás előtt
- **Nyomkövetés**: Minden hiba tartalmazza az eredeti kivételt

## Használat

### Alapvető használat

```python
from datetime import datetime
from neural_ai.core.processing.resampler_service import ResamplerServiceFactory

# Factory példányosítása
factory = ResamplerServiceFactory()

# ResamplerService példány létrehozása
resampler = factory.get_instance()

# Tick adatok átalakítása OHLCV gyertyákká
symbol = "EURUSD"
start = datetime(2024, 1, 1)
end = datetime(2024, 1, 31)
timeframe = "1h"

ohlcv_data = await resampler.resample(
    symbol=symbol,
    start=start,
    end=end,
    timeframe=timeframe
)
```

### Manuális létrehozás

```python
from neural_ai.core.storage.factory import StorageFactory
from neural_ai.core.processing.resampler_service import ResamplerServiceFactory

# Storage létrehozása
storage = StorageFactory.get_storage(storage_type="parquet")

# ResamplerService létrehozása
resampler = ResamplerServiceFactory.create(storage=storage)
```

## Hibakezelés

A ResamplerService három fő kategóriájú kivételt dobhat:

### 1. InvalidTimeframeError

Akkor dobódik, ha érvénytelen időkeretet adunk meg.

```python
try:
    ohlcv = await resampler.resample(symbol, start, end, "invalid_tf")
except InvalidTimeframeError as e:
    print(f"Érvénytelen időkeret: {e.details}")
```

### 2. DataLoadError

Akkor dobódik, ha hiba történik az adatok betöltése során.

```python
try:
    ohlcv = await resampler.resample(symbol, start, end, "1h")
except DataLoadError as e:
    print(f"Adatbetöltési hiba: {e.message}")
    print(f"Részletek: {e.details}")
```

### 3. ResamplingError

Akkor dobódik, ha hiba történik az átalakítás során.

```python
try:
    ohlcv = await resampler.resample(symbol, start, end, "1h")
except ResamplingError as e:
    print(f"Átalakítási hiba: {e.message}")
    print(f"Eredeti hiba: {e.original_error}")
```

## Implementáció részletei

### Adatfolyam

1. **Validáció**: Az időkeret ellenőrzése
2. **Betöltés**: Tick adatok betöltése a tárolóból
3. **Átalakítás**: Tick → OHLCV konverzió
4. **Visszaadás**: Pandas DataFrame formátumban

### OHLCV számítás

- **Open**: Az időkeret első tick ára
- **High**: A legmagasabb ár az időkeretben
- **Low**: A legalacsonyabb ár az időkeretben
- **Close**: Az utolsó tick ára
- **Volume**: A kötetek összege az időkeretben

### Teljesítmény optimalizációk

- **Group By Dynamic**: Polars `group_by_dynamic` használata
- **Lazy Evaluation**: A számítások késleltetett kiértékelése
- **Batch Processing**: Kötegelt feldolgozás nagy adatmennyiségekhez

## Függőségek

- `pandas`: DataFrame kezelés
- `polars`: Nagy teljesítményű adatfeldolgozás
- `numpy`: Numerikus műveletek
- `neural_ai.core.storage`: Adattárolási réteg

## Jövőbeli fejlesztések

- [ ] Több adatforrás támogatása
- [ ] Egyéni aggregációs függvények
- [ ] Real-time resampling streameléshez
- [ ] Gyorsítótár-rendszer a gyakran használt időkeretekhez
- [ ] Parallel processing nagy adatmennyiségekhez

## Kapcsolódó dokumentáció

- [Factory](factory.md)
- [Interfaces](interfaces/resampler_interface.md)
- [Implementations](implementations/resampler_service.md)
- [Exceptions](exceptions/resampler_error.md)