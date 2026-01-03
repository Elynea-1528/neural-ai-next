# ResamplerService Kivételek

## Áttekintés

A `ResamplerService` modul egyéni kivétel hierarchiát használ a hibakezeléshez. Minden kivétel a `NeuralAIException` alaposztályból származik, ami biztosítja a konzisztens hibakezelést és a részletes hibainformációkat.

## Kivétel hierarchia

```
NeuralAIException
└── ResamplerError
    ├── DataLoadError
    ├── ResamplingError
    └── InvalidTimeframeError
```

## Alap kivétel: ResamplerError

### Osztály definíció

```python
class ResamplerError(NeuralAIException):
    """Alapértelmezett hiba a ResamplerService-hez."""
    
    def __init__(
        self,
        message: str,
        details: str | None = None,
        original_error: Exception | None = None
    ):
        """ResamplerError inicializálása.
        
        Args:
            message: A hibaüzenet
            details: Részletes hibainformációk
            original_error: Az eredeti kivétel (ha van)
        """
        super().__init__(message)
        self.details = details
        self.original_error = original_error
        self.component = "ResamplerService"
```

### Attribútumok

| Attribútum | Típus | Leírás |
|------------|-------|---------|
| `message` | `str` | A hibaüzenet |
| `details` | `str \| None` | Részletes hibainformációk |
| `original_error` | `Exception \| None` | Az eredeti kivétel |
| `component` | `str` | A komponens neve ("ResamplerService") |

### Példa használat

```python
try:
    result = await resampler.resample(symbol, start, end, timeframe)
except ResamplerError as e:
    print(f"Hiba: {e.message}")
    print(f"Részletek: {e.details}")
    if e.original_error:
        print(f"Eredeti hiba: {e.original_error}")
```

## DataLoadError

### Leírás

A `DataLoadError` akkor dobódik, ha hiba történik az adatok betöltése során a tárolóból.

### Osztály definíció

```python
class DataLoadError(ResamplerError):
    """Hiba adatok betöltése során."""
    
    def __init__(
        self,
        symbol: str,
        start: str,
        end: str,
        original_error: Exception | None = None
    ):
        """DataLoadError inicializálása.
        
        Args:
            symbol: A kereskedési szimbólum
            start: A kezdő időpont
            end: A záró időpont
            original_error: Az eredeti kivétel
        """
        message = f"Adatok betöltése sikertelen a(z) {symbol} szimbólumhoz"
        details = f"Időintervallum: {start} - {end}"
        super().__init__(
            message=message,
            details=details,
            original_error=original_error
        )
```

### Attribútumok

| Attribútum | Típus | Leírás |
|------------|-------|---------|
| `symbol` | `str` | A kereskedési szimbólum |
| `start` | `str` | A kezdő időpont |
| `end` | `str` | A záró időpont |

### Példa

```python
from neural_ai.core.processing.resampler_service.exceptions.resampler_error import (
    DataLoadError,
)

try:
    tick_data = await self._load_tick_data(symbol, start, end)
except Exception as e:
    raise DataLoadError(
        symbol=symbol,
        start=str(start),
        end=str(end),
        original_error=e
    ) from e
```

### Hibakezelés

```python
try:
    result = await resampler.resample(symbol, start, end, timeframe)
except DataLoadError as e:
    print(f"Adatbetöltési hiba: {e.message}")
    print(f"Szimbólum: {e.symbol}")
    print(f"Időintervallum: {e.details}")
    # További hibakezelés
```

## ResamplingError

### Leírás

A `ResamplingError` akkor dobódik, ha hiba történik az adatok átalakítása (resampling) során.

### Osztály definíció

```python
class ResamplingError(ResamplerError):
    """Hiba az adatok átalakítása (resampling) során."""
    
    def __init__(
        self,
        symbol: str,
        timeframe: str,
        original_error: Exception | None = None
    ):
        """ResamplingError inicializálása.
        
        Args:
            symbol: A kereskedési szimbólum
            timeframe: Az időkeret
            original_error: Az eredeti kivétel
        """
        message = f"Az adatok átalakítása sikertelen a(z) {symbol} szimbólumhoz"
        details = f"Időkeret: {timeframe}"
        super().__init__(
            message=message,
            details=details,
            original_error=original_error
        )
```

### Attribútumok

| Attribútum | Típus | Leírás |
|------------|-------|---------|
| `symbol` | `str` | A kereskedési szimbólum |
| `timeframe` | `str` | Az időkeret |

### Példa

```python
from neural_ai.core.processing.resampler_service.exceptions.resampler_error import (
    ResamplingError,
)

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

### Hibakezelés

```python
try:
    result = await resampler.resample(symbol, start, end, timeframe)
except ResamplingError as e:
    print(f"Átalakítási hiba: {e.message}")
    print(f"Időkeret: {e.timeframe}")
    # További hibakezelés
```

## InvalidTimeframeError

### Leírás

A `InvalidTimeframeError` akkor dobódik, ha érvénytelen időkeretet adunk meg a resample metódusnak.

### Osztály definíció

```python
class InvalidTimeframeError(ResamplerError):
    """Hiba érvénytelen időkeret esetén."""
    
    def __init__(self, timeframe: str):
        """InvalidTimeframeError inicializálása.
        
        Args:
            timeframe: Az érvénytelen időkeret
        """
        message = f"Érvénytelen időkeret: {timeframe}"
        details = (
            "Az időkeretnek a Pandas offset formátumban kell lennie "
            "(pl. '1m', '5m', '1h', '1D')"
        )
        super().__init__(message=message, details=details)
```

### Attribútumok

| Attribútum | Típus | Leírás |
|------------|-------|---------|
| `timeframe` | `str` | Az érvénytelen időkeret |

### Példa

```python
from neural_ai.core.processing.resampler_service.exceptions.resampler_error import (
    InvalidTimeframeError,
)

def _validate_timeframe(self, timeframe: str) -> None:
    valid_timeframes = ['1m', '5m', '15m', '30m', '1h', '4h', '1D', '1W', '1M']
    if timeframe not in valid_timeframes:
        raise InvalidTimeframeError(timeframe)
```

### Hibakezelés

```python
try:
    result = await resampler.resample(symbol, start, end, "invalid_tf")
except InvalidTimeframeError as e:
    print(f"Érvénytelen időkeret: {e.message}")
    print(f"Részletek: {e.details}")
    # További hibakezelés
```

## Támogatott időkeretek

A következő időkeretek érvényesek:

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

## Hibakezelési minta

### Komplex hibakezelés

```python
from neural_ai.core.processing.resampler_service.exceptions.resampler_error import (
    DataLoadError,
    InvalidTimeframeError,
    ResamplingError,
)

async def process_data(symbol, start, end, timeframe):
    """Komplex hibakezelés példa."""
    try:
        result = await resampler.resample(symbol, start, end, timeframe)
        return result
    
    except InvalidTimeframeError as e:
        # Érvénytelen időkeret
        logger.error(f"Érvénytelen időkeret: {e.timeframe}")
        # Felhasználói visszajelzés
        return None
    
    except DataLoadError as e:
        # Adatbetöltési hiba
        logger.error(f"Adatbetöltési hiba: {e.message}")
        logger.error(f"Részletek: {e.details}")
        # Újrapróbálkozás logika
        return await retry_load(symbol, start, end)
    
    except ResamplingError as e:
        # Átalakítási hiba
        logger.error(f"Átalakítási hiba: {e.message}")
        logger.error(f"Eredeti hiba: {e.original_error}")
        # Alternatív feldolgozás
        return await alternative_processing(symbol, start, end, timeframe)
    
    except Exception as e:
        # Egyéb váratlan hibák
        logger.error(f"Váratlan hiba: {e}")
        raise
```

### Logolás

```python
import logging

logger = logging.getLogger(__name__)

try:
    result = await resampler.resample(symbol, start, end, timeframe)
except ResamplerError as e:
    logger.error(f"Resampler hiba: {e.message}")
    logger.error(f"Részletek: {e.details}")
    if e.original_error:
        logger.exception(e.original_error)
```

## Kapcsolódó dokumentáció

- [ResamplerService](../index.md)
- [ResamplerInterface](../interfaces/resampler_interface.md)
- [ResamplerService Implementation](../implementations/resampler_service.md)
- [ResamplerService Factory](../factory.md)