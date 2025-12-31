# ResamplerError

## Áttekintés

A `ResamplerError` és leszármazottai a ResamplerService által dobott kivételeket reprezentálják. Ezek a kivételek részletes hibainformációkat szolgáltatnak a tick adatok OHLCV gyertyákká alakítása során fellépő problémákról.

## Kivétel hierarchia

```
NeuralAIException
└── ResamplerError
    ├── DataLoadError
    ├── ResamplingError
    └── InvalidTimeframeError
```

## Alap kivétel

### `ResamplerError`

Alapértelmezett hiba a ResamplerService-hez.

```python
class ResamplerError(NeuralAIException)
```

**Konstruktor:**

```python
def __init__(
    self,
    message: str,
    details: Optional[str] = None,
    original_error: Optional[Exception] = None
)
```

**Attribútumok:**

- `message` (str): A hibaüzenet
- `details` (Optional[str]): Részletes hibainformációk
- `original_error` (Optional[Exception]): Az eredeti kivétel
- `component` (str): A komponens neve ("ResamplerService")

## Specifikus kivételek

### `DataLoadError`

Hiba adatok betöltése során.

```python
class DataLoadError(ResamplerError)
```

**Konstruktor:**

```python
def __init__(
    self,
    symbol: str,
    start: str,
    end: str,
    original_error: Optional[Exception] = None
)
```

**Példa:**

```python
try:
    tick_data = await storage.load_tick_data("EURUSD", start, end)
except Exception as e:
    raise DataLoadError(
        symbol="EURUSD",
        start=str(start),
        end=str(end),
        original_error=e
    )
```

### `ResamplingError`

Hiba az adatok átalakítása (resampling) során.

```python
class ResamplingError(ResamplerError)
```

**Konstruktor:**

```python
def __init__(
    self,
    symbol: str,
    timeframe: str,
    original_error: Optional[Exception] = None
)
```

**Példa:**

```python
try:
    ohlcv_data = self._convert_to_ohlcv(tick_data, timeframe)
except Exception as e:
    raise ResamplingError(
        symbol="EURUSD",
        timeframe="1m",
        original_error=e
    )
```

### `InvalidTimeframeError`

Hiba érvénytelen időkeret esetén.

```python
class InvalidTimeframeError(ResamplerError)
```

**Konstruktor:**

```python
def __init__(self, timeframe: str)
```

**Példa:**

```python
if timeframe not in valid_timeframes:
    raise InvalidTimeframeError(timeframe)
```

## Használati példa

```python
from neural_ai.core.storage.services.resampler_service.exceptions import (
    ResamplerError,
    DataLoadError,
    ResamplingError,
    InvalidTimeframeError
)

try:
    resampler = ResamplerServiceFactory.get_instance()
    ohlcv_data = await resampler.resample(
        symbol="EURUSD",
        start=start,
        end=end,
        timeframe="1m"
    )
except InvalidTimeframeError as e:
    print(f"Érvénytelen időkeret: {e}")
except DataLoadError as e:
    print(f"Adatok betöltése sikertelen: {e}")
    print(f"Részletek: {e.details}")
except ResamplingError as e:
    print(f"Átalakítás sikertelen: {e}")
    print(f"Eredeti hiba: {e.original_error}")
except ResamplerError as e:
    print(f"Általános resampler hiba: {e}")
```

## Hibakezelés

### Hibák ellenőrzése

```python
# Komponens ellenőrzése
if error.component == "ResamplerService":
    # ResamplerService hibája
    pass

# Részletek lekérdezése
if error.details:
    print(f"Részletek: {error.details}")

# Eredeti hiba ellenőrzése
if error.original_error:
    print(f"Eredeti hiba: {error.original_error}")
```

### Hibanaplózás

```python
import logging

logger = logging.getLogger(__name__)

try:
    # ResamplerService művelet
    pass
except ResamplerError as e:
    logger.error(
        f"ResamplerService hiba: {e.message}",
        extra={
            "component": e.component,
            "details": e.details,
            "original_error": str(e.original_error) if e.original_error else None
        }
    )
```

## Lásd még

- [ResamplerInterface](../interfaces/resampler_interface.md)
- [ResamplerService](../implementations/resampler_service.md)
- [ResamplerServiceFactory](../factory.md)