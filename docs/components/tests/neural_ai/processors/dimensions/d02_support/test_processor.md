# tests/neural_ai/processors/dimensions/d02_support/test_processor.py

Tests for D02 Support Processor.

## Importok

```python
from unittest.mock import MagicMock
import polars
import pytest
from pydantic import ValidationError
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.config.interfaces.types import ProcessorConfig
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
from neural_ai.processors.dimensions.d02_support.implementations.support_processor import D02SupportProcessor
```

## Konstansok

- **`config`**
: `MagicMock(spec=ConfigManagerInterface)`


- **`logger`**
: `MagicMock(spec=LoggerInterface)`


- **`processor`**
: `D02SupportProcessor(config, logger)`


- **`processor`**
: `D02SupportProcessor(config, logger)`


- **`df`**
: `pl.DataFrame({'timestamp': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'mid_open': [1.0] * 10, 'mid_high': [1.1] * 10, 'mid_low': [0.9] * 10, 'mid_close': [1.0] * 10, 'real_volume': [100.0] * 10})`


- **`df`**
: `df.with_columns(pl.datetime(2024, 1, 1).alias('timestamp'))`


- **`result`**
: `processor.process(df)`


### `mock_deps()`

```python
def mock_deps()
```

Create mock dependencies.

### `test_d02_processor_happy_path()`

```python
def test_d02_processor_happy_path(mock_deps)
```

Test D02SupportProcessor instantiation with valid config.

**Paraméterek:**

- **`mock_deps`**

### `test_d02_processor_defaults()`

```python
def test_d02_processor_defaults(mock_deps)
```

Test D02SupportProcessor default values.

**Paraméterek:**

- **`mock_deps`**

### `test_d02_processor_validation_error()`

```python
def test_d02_processor_validation_error(mock_deps)
```

Test D02SupportProcessor with invalid config.

**Paraméterek:**

- **`mock_deps`**

### `test_d02_processor_invalid_type()`

```python
def test_d02_processor_invalid_type(mock_deps)
```

Test D02SupportProcessor with invalid type in config.

**Paraméterek:**

- **`mock_deps`**

---

**Forrásfájl:** [`tests/neural_ai/processors/dimensions/d02_support/test_processor.py`](../../tests/neural_ai/processors/dimensions/d02_support/test_processor.py)
