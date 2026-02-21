# tests/scripts/test_test_tick_pipeline.py

Test Tick Pipeline szkript teszt modul.

Ez a modul tartalmazza a test_tick_pipeline.py szkript tesztjeit.

## Importok

```python
from unittest.mock import MagicMock
from unittest.mock import patch
from scripts.test_tick_pipeline import validate_tick_pipeline
from datetime import datetime
import polars
```

## Osztály: `TestValidateTickPipeline`

Test Tick Pipeline szkript tesztek.

### Metódusok

#### `test_validate_tick_pipeline_success()`

```python
def test_validate_tick_pipeline_success(self)
```

Teszt sikeres tick pipeline validáció.

**Paraméterek:**

- **`self`**

#### `mock_resample()`

```python
async def mock_resample()
```

#### `mock_process()`

```python
async def mock_process()
```

#### `test_validate_tick_pipeline_resample_failure()`

```python
def test_validate_tick_pipeline_resample_failure(self)
```

Teszt resample hiba esetén.

**Paraméterek:**

- **`self`**

#### `test_validate_tick_pipeline_d1_failure()`

```python
def test_validate_tick_pipeline_d1_failure(self)
```

Teszt D1 processor hiba esetén.

**Paraméterek:**

- **`self`**

#### `test_validate_tick_pipeline_validation_failure()`

```python
def test_validate_tick_pipeline_validation_failure(self)
```

Teszt validációs hiba esetén.

**Paraméterek:**

- **`self`**

#### `test_validate_tick_pipeline_validation_errors()`

```python
def test_validate_tick_pipeline_validation_errors(self)
```

Teszt különböző validációs hibák esetén.

**Paraméterek:**

- **`self`**

---

**Forrásfájl:** [`tests/scripts/test_test_tick_pipeline.py`](../../tests/scripts/test_test_tick_pipeline.py)
