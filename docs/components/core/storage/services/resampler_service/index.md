# ResamplerService

## Áttekintés

A `ResamplerService` egy kritikus komponens a Neural AI Next rendszerben, amely tick adatokból hoz létre OHLCV (Open, High, Low, Close, Volume) gyertyákat. Ez a szolgáltatás alapja az adatfeldolgozási pipeline-nak, válaszolva a "hogy lesz ebből gyertya" kérdésre az OMEGA PROTOCOL kontextusában.

## Főbb jellemzők

- **Tick → OHLCV átalakítás**: Nagy teljesítményű átalakítás Polars segítségével
- **Több időkeret támogatása**: 1m, 5m, 15m, 30m, 1h, 4h, 1D, 1W, 1M
- **Dependency Injection**: Tiszta architektúra a StorageInterface függőséggel
- **Hibatűrő**: Átfogó hibakezelés specifikus kivételekkel
- **Big Data támogatás**: Hatékony feldolgozás nagy adatmennyiségekhez

## Architektúra

A modul a szabványos Neural AI Next architektúrát követi:

```
resampler_service/
├── interfaces/
│   └── resampler_interface.py      # ABC interfész
├── implementations/
│   └── resampler_service.py        # Fő implementáció
├── exceptions/
│   └── resampler_error.py          # Specifikus kivételek
├── factory.py                      # Factory osztály
└── __init__.py                     # Modul exportálás
```

## Gyors kezdés

### Telepítés

```python
from neural_ai.core.storage.services.resampler_service import (
    ResamplerServiceFactory,
    ResamplerInterface
)
```

### Alap használat

```python
from datetime import datetime

# ResamplerService példány létrehozása
resampler: ResamplerInterface = ResamplerServiceFactory.get_instance()

# Tick adatok átalakítása 1 perces gyertyákká
start = datetime(2024, 1, 1, 0, 0, 0)
end = datetime(2024, 1, 1, 23, 59, 59)

ohlcv_data = await resampler.resample(
    symbol="EURUSD",
    start=start,
    end=end,
    timeframe="1m"
)

print(f"Létrejött {len(ohlcv_data)} gyertya")
```

## Komponensek

### 1. ResamplerInterface

Az interfész, amely definiálja a resampling műveleteket.

**Főbb metódusok:**

- `resample()`: Tick adatok átalakítása OHLCV gyertyákká

**Lásd:** [ResamplerInterface](interfaces/resampler_interface.md)

### 2. ResamplerService

A fő implementáció, amely Polars-t használ a nagy teljesítményű feldolgozáshoz.

**Főbb jellemzők:**

- Polars alapú aggregáció
- Több időkeret támogatása
- Memóriahatékony feldolgozás

**Lásd:** [ResamplerService](implementations/resampler_service.md)

### 3. ResamplerServiceFactory

Factory osztály a ResamplerService létrehozásához és kezeléséhez.

**Főbb metódusok:**

- `create()`: Példány létrehozása
- `get_instance()`: Singleton példány lekérése

**Lásd:** [ResamplerServiceFactory](factory.md)

### 4. ResamplerError

Kivétel hierarchia a resampling hibák kezeléséhez.

**Kivétel típusok:**

- `DataLoadError`: Adatok betöltése során fellépő hibák
- `ResamplingError`: Adatok átalakítása során fellépő hibák
- `InvalidTimeframeError`: Érvénytelen időkeret esetén

**Lásd:** [ResamplerError](exceptions/resampler_error.md)

## Használati példák

### 1. Egyszerű resampling

```python
from datetime import datetime
from neural_ai.core.storage.services.resampler_service import (
    ResamplerServiceFactory,
    ResamplerInterface
)

resampler: ResamplerInterface = ResamplerServiceFactory.get_instance()

# 5 perces gyertyák létrehozása
ohlcv_5m = await resampler.resample(
    symbol="EURUSD",
    start=datetime(2024, 1, 1, 0, 0, 0),
    end=datetime(2024, 1, 1, 23, 59, 59),
    timeframe="5m"
)
```

### 2. Több időkeret feldolgozása

```python
import asyncio

timeframes = ["1m", "5m", "15m", "1h", "4h"]
results = {}

for tf in timeframes:
    ohlcv = await resampler.resample(
        symbol="EURUSD",
        start=start,
        end=end,
        timeframe=tf
    )
    results[tf] = ohlcv
```

### 3. Hibakezelés

```python
from neural_ai.core.storage.services.resampler_service.exceptions import (
    DataLoadError,
    ResamplingError,
    InvalidTimeframeError
)

try:
    ohlcv_data = await resampler.resample(
        symbol="EURUSD",
        start=start,
        end=end,
        timeframe="1m"
    )
except InvalidTimeframeError as e:
    print(f"Érvénytelen időkeret: {e}")
except DataLoadError as e:
    print(f"Adatok betöltése sikertelen: {e.details}")
except ResamplingError as e:
    print(f"Átalakítás sikertelen: {e}")
```

## Technológiai háttér

### Polars integráció

A ResamplerService Polars-t használ a nagy teljesítményű adatfeldolgozáshoz:

- **`group_by_dynamic()`**: Dinamikus csoportosítás időalapú ablakokban
- **Hatékony aggregáció**: `first()`, `max()`, `min()`, `last()`, `sum()`
- **Lazy evaluation**: Memóriahatékony feldolgozás

### OHLCV számítás

1. **Átlagár**: `price = (bid + ask) / 2`
2. **Csoportosítás**: Időkeret szerinti csoportosítás
3. **Aggregáció**:
   - Open: Első ár
   - High: Legmagasabb ár
   - Low: Legalacsonyabb ár
   - Close: Utolsó ár
   - Volume: Volumen összeg

## Támogatott időkeretek

| Időkeret | Leírás |
|----------|--------|
| `1m` | 1 perc |
| `5m` | 5 perc |
| `15m` | 15 perc |
| `30m` | 30 perc |
| `1h` | 1 óra |
| `4h` | 4 óra |
| `1D` | 1 nap |
| `1W` | 1 hét |
| `1M` | 1 hónap |

## Teljesítmény

A ResamplerService a következő teljesítményoptimalizálásokat használja:

- **Polars motor**: Nagy teljesítményű DataFrame feldolgozás
- **Aszinkron műveletek**: Nem blokkoló I/O műveletek
- **Memóriahatékony**: Lazy evaluation és chunkolás
- **Párhuzamos feldolgozás**: Több szimbólum egyidejű feldolgozása

## Fejlesztés

### Tesztelés

```bash
# Egyedi teszt futtatása
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/core/storage/services/test_resampler_service.py -v

# Coverage ellenőrzés
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/core/storage/services/test_resampler_service.py --cov=neural_ai.core.storage.services.resampler_service --cov-report=term-missing
```

### Linter ellenőrzés

```bash
/home/elynea/miniconda3/envs/neural-ai-next/bin/ruff check neural_ai/core/storage/services/resampler_service/
```

## Kapcsolódó komponensek

- [StorageInterface](../../interfaces/storage_interface.md): A tárolási réteg interfésze
- [ParquetStorageService](../../implementations/parquet_storage.md): Parquet alapú tárolás
- [DIContainer](../../../base/implementations/di_container.md): Dependency Injection konténer

## API referencia

A teljes API dokumentációért lásd:

- [ResamplerInterface](interfaces/resampler_interface.md)
- [ResamplerService](implementations/resampler_service.md)
- [ResamplerServiceFactory](factory.md)
- [ResamplerError](exceptions/resampler_error.md)