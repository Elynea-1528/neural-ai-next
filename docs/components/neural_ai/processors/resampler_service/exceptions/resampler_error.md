# neural_ai/processors/resampler_service/exceptions/resampler_error.py

ResamplerService kivételek.

## Importok

```python
from neural_ai.core.base.exceptions.base_error import NeuralAIException
```

## Osztály: `ResamplerError(NeuralAIException)`

Alapértelmezett hiba a ResamplerService-hez.

### Metódusok

#### `__init__()`

```python
def __init__(self, message: str, details: str | None = None, original_error: Exception | None = None)
```

ResamplerError inicializálása.

**Paraméterek:**

- **`self`**
- **`message`** (`str`): A hibaüzenet
- **`details`** (`str | None`) = `None`: Részletes hibainformációk
- **`original_error`** (`Exception | None`) = `None`: Az eredeti kivétel (ha van)

## Osztály: `DataLoadError(ResamplerError)`

Hiba adatok betöltése során.

### Metódusok

#### `__init__()`

```python
def __init__(self, symbol: str, start: str, end: str, original_error: Exception | None = None)
```

DataLoadError inicializálása.

**Paraméterek:**

- **`self`**
- **`symbol`** (`str`): A kereskedési szimbólum
- **`start`** (`str`): A kezdő időpont
- **`end`** (`str`): A záró időpont
- **`original_error`** (`Exception | None`) = `None`: Az eredeti kivétel

## Osztály: `ResamplingError(ResamplerError)`

Hiba az adatok átalakítása (resampling) során.

### Metódusok

#### `__init__()`

```python
def __init__(self, symbol: str, timeframe: str, original_error: Exception | None = None)
```

ResamplingError inicializálása.

**Paraméterek:**

- **`self`**
- **`symbol`** (`str`): A kereskedési szimbólum
- **`timeframe`** (`str`): Az időkeret
- **`original_error`** (`Exception | None`) = `None`: Az eredeti kivétel

## Osztály: `InvalidTimeframeError(ResamplerError)`

Hiba érvénytelen időkeret esetén.

### Metódusok

#### `__init__()`

```python
def __init__(self, timeframe: str)
```

InvalidTimeframeError inicializálása.

**Paraméterek:**

- **`self`**
- **`timeframe`** (`str`): Az érvénytelen időkeret

---

**Forrásfájl:** [`neural_ai/processors/resampler_service/exceptions/resampler_error.py`](../../neural_ai/processors/resampler_service/exceptions/resampler_error.py)
