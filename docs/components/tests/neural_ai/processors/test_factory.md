# tests/neural_ai/processors/test_factory.py

Tests for Processor Factory.

## Importok

```python
from unittest.mock import MagicMock
import pytest
from pydantic import ValidationError
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
from neural_ai.processors.dimensions.d02_support.implementations.support_processor import D02SupportProcessor
from neural_ai.processors.factory import create_dimension_processor
from neural_ai.processors.interfaces.dimension_processor_interface import IDimensionProcessor
```

## Konstansok

- **`mock_config`**
: `MagicMock(spec=ConfigManagerInterface)`


- **`mock_logger`**
: `MagicMock(spec=LoggerInterface)`


- **`processor`**
: `create_dimension_processor(2, mock_config, mock_logger)`


- **`mock_config`**
: `MagicMock(spec=ConfigManagerInterface)`


- **`mock_logger`**
: `MagicMock(spec=LoggerInterface)`


- **`mock_config`**
: `MagicMock(spec=ConfigManagerInterface)`


- **`mock_logger`**
: `MagicMock(spec=LoggerInterface)`


### `test_create_dimension_processor_happy_path()`

```python
def test_create_dimension_processor_happy_path()
```

Test create_dimension_processor with valid config.

### `config_get_side_effect()`

```python
def config_get_side_effect(section, key = None)
```

**Paraméterek:**

- **`section`**
- **`key`** = `None`

### `test_create_dimension_processor_validation_error()`

```python
def test_create_dimension_processor_validation_error()
```

Test create_dimension_processor with invalid config.

### `config_get_side_effect()`

```python
def config_get_side_effect(section, key = None)
```

**Paraméterek:**

- **`section`**
- **`key`** = `None`

### `test_create_dimension_processor_invalid_id()`

```python
def test_create_dimension_processor_invalid_id()
```

Test create_dimension_processor with unknown dimension ID.

---

**Forrásfájl:** [`tests/neural_ai/processors/test_factory.py`](../../tests/neural_ai/processors/test_factory.py)
