# neural_ai/processors/factory.py

Processing Factory - Feldolgozási komponensek factory függvényei.

## Importok

```python
import importlib
from typing import TYPE_CHECKING
from typing import cast
from pydantic import ValidationError
from neural_ai.core.config.interfaces.types import ProcessorsConfig
from neural_ai.processors.interfaces.dimension_processor_interface import IDimensionProcessor
from neural_ai.processors.interfaces.time_alignment_interface import ITimeAlignmentService
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
from typing import cast
```

## Konstansok

- **`DIMENSIONS_CONFIG`**
: `{1: 'price', 2: 'support'}`


- **`FACTORY_CLASSES`**
: `{1: 'D01PriceFactory', 2: 'D02SupportFactory'}`


- **`module`**
: `importlib.import_module('neural_ai.processors.implementations.time_alignment_service')`


- **`cls`**
: `module.TimeAlignmentService`


- **`name`**
: `DIMENSIONS_CONFIG[dimension_id]`


- **`module_name`**
: `f'neural_ai.processors.dimensions.d{dimension_id:02d}_{name}.factory'`


- **`module`**
: `importlib.import_module(module_name)`


- **`factory_class`**
: `getattr(module, FACTORY_CLASSES[dimension_id])`


### `create_time_alignment_service()`

```python
def create_time_alignment_service(config: 'ConfigManagerInterface', logger: 'LoggerInterface') -> ITimeAlignmentService
```

TimeAlignmentService factory függvény - dinamikus példányosítással.

**Paraméterek:**

- **`config`** (`'ConfigManagerInterface'`): Konfigurációs menedzser interfész
- **`logger`** (`'LoggerInterface'`): A naplózási interfész.

**Visszatérési érték:**

- Típus: `ITimeAlignmentService`
- ITimeAlignmentService: Az időszinkronizációs szolgáltatás példánya

### `create_dimension_processor()`

```python
def create_dimension_processor(dimension_id: int, config: 'ConfigManagerInterface', logger: 'LoggerInterface') -> IDimensionProcessor
```

Dimenzió processzor factory függvény - dinamikus factory loadinggal.

**Paraméterek:**

- **`dimension_id`** (`int`): A dimenzió azonosítója (1-15)
- **`config`** (`'ConfigManagerInterface'`): Konfigurációs menedzser interfész
- **`logger`** (`'LoggerInterface'`): Logger interfész

**Visszatérési érték:**

- Típus: `IDimensionProcessor`
- IDimensionProcessor: A megfelelő dimenzió processor példány

**Kivételek:**

- **`ValueError`**: Ha ismeretlen dimenzió ID-t adnak meg

---

**Forrásfájl:** [`neural_ai/processors/factory.py`](../../neural_ai/processors/factory.py)
